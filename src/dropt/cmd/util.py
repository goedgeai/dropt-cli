import questionary
from dropt.client.util import is_int
import importlib.util
import os
import sys
import json
from datetime import datetime, timezone
from time import sleep
from pathlib import Path


PCACHE_DIR = Path('.dropt/projects')


class ProjectCache:
    '''Project cache.'''
    def __init__(self, project_id, n_trial, config):
        # create directory if it does not exist
        try:
            PCACHE_DIR.mkdir(parents=True, exist_ok=True)
        except FileExistsError as e:
            print('Directory path conflicts with an existing regular file: {e}')
            sys.exit(1)

        self.filename = PCACHE_DIR.joinpath(f'{project_id}.json')
        self.project_id = project_id
        self.n_trial = n_trial
        self.config = config
        self.create_time = datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()
        self.progress = 0
        self.status = 'pending'

    def _to_dict(self):
        d = self.__dict__.copy()
        d.pop('filename')
        d.pop('model')
        return d

    def save(self):
        with open(self.filename, 'w') as f:
            json.dump(self._to_dict(), f)

    def load(self):
        with open(self.filename, 'r') as f:
            self.__dict__.update(json.load(f))

    def load_model(self):
        '''Load model.'''
        name = self.config['config']['model']
        spec = importlib.util.spec_from_file_location(name, f'{name}.py')
        self.model = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.model)

    def kill(self, signal):
        if signal == 'update':
            if self.status == 'running':
                self.progress += 1
                if self.progress == self.n_trial:
                    self.status = 'done'
            else:
                raise RuntimeError(f'Project (id={self.project_id}) is not running.')
        elif signal == 'start':
            if self.status == 'pending':
                self.status = 'running'
            else:
                raise RuntimeError(f'Project (id={self.project_id}) is not pending.')
        elif signal == 'kill':
            self.status = 'killed'
        else:
            raise ValueError('Unknown signal.')


def header_footer_loop(func):
    '''Decorator tha includes header, footer and trial loop for projects.'''
    def wrapper(project, pcache):
        # header
        print(f'\n=================== Trial Start ====================')
        print(f'\t\tProject ID: {pcache.project_id}')
        print(f'----------------------------------------------------')

        # load model
        pcache.load_model()

        # send start signal
        pcache.kill('start')

        # trial loop
        for i in range(pcache.progress, pcache.n_trial):
            print(f'\n[trial {i+1}/{pcache.n_trial}]')
            func(project, pcache)
        
        # footer
        print('\n=================== Trial End ======================\n')
    return wrapper


@header_footer_loop
def search_parameter(project, pcache):
    '''Parameter search and evaluation.'''
    # wait for back-end processing
    sleep(2)

    # request hyper-parameters from DrOpt
    sugt = project.suggestions().create()
    sugt_id = sugt.suggest_id
    sugt_value = sugt.assignments

    # evaluate the model with the suggested parameter configuration
    params = pcache.config['params']
    params.update(sugt_value)
    print(f'Suggestion = {sugt_value}')
    try:
        metric = pcache.model.run(params)
    except RuntimeError as e:
        print(e)
        print('Please add RuntimeError handler in your model code.')
        sys.exit(1)
    print(f'Evaluation: {metric}')

    # report result to DrOpt
    project.validations().create(suggest_id=sugt_id, value=metric)

    # update project_log
    pcache.kill('update')
    pcache.save()


def resume_prompt():
    '''Get the resume project_id. 
    Users can select from exist progress files or input the project_id manually.

    Returns:
        project_id    - id of the selected project
        file_progress - progress of the selected local file
    '''

    def get_proj_id_input():
        if questionary.confirm('Would you like to specify a project_id?').ask():
            proj_id = questionary.text('The project_id you would like to resume:').ask()
            if is_int(proj_id) != True:
                print('\nThe project_id must be an integer! droptctl exited.')
                sys.exit(1)
        else:
            print('\ndroptctl exited.')
            exit(1)
        return proj_id

    # read resume files
    if (PCACHE_DIR.is_dir() != True):
        print('\n! The project cache directory does not exist.\n')
        proj_id = int(get_proj_id_input())
        return proj_id
    else:
        project_files = []
        for f in PCACHE_DIR.glob('*'):
            with open(f) as fh:
                project_files.append(json.load(fh)) 

        project_files = sorted(project_files, key=lambda k: k['create_time'], reverse=True) 
        choices =  [(f"[project {p['project_id']}] "
                     f"name: {p['name']}, "
                     f"progress: {p['progress']+1}, "
                     f"create_time: {p['create_time']}")
                         for p in project_files if p.get('status') == 'running']
        
        if len(choices) == 0:
            print("\n! There does not exist any running project in this dir.\n")
            proj_id = int(get_proj_id_input())
            return proj_id
        
        user_answer = questionary.select(
            "Which project would you like to resume?",
            choices = choices
        ).ask()

        if user_answer == None:
            print("droptctl exited.")
            exit(0)

        return int(user_answer.split(']')[0].split('project ')[1]),\
               int(user_answer.split('progress: ')[1].split(', create_time')[0])
