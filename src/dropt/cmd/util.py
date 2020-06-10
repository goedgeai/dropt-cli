import questionary
import importlib.util
import sys
import json
from datetime import datetime, timezone
from time import sleep
from pathlib import Path
from dropt.util.log import CliLogger


PCACHE_DIR = Path('.dropt/pcache')


class ProjectCache:
    '''Project cache.'''
    def __init__(self, pid, name=None, n_trial=None, model_file=None, model_params=None):
        # create cache directory
        PCACHE_DIR.mkdir(parents=True, exist_ok=True)

        self.pid = pid
        self.name = name
        self.n_trial = n_trial
        self._model_file = model_file
        self.model_params = model_params
        self.create_time = datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()
        self.progress = 0
        self.status = 'pending'

    @property
    def model_file(self):
        return Path(self._model_file)

    @property
    def cache_file(self):
        return PCACHE_DIR.joinpath(f'{self.pid}.json')

    def save(self):
        '''Save project cache.'''
        with open(self.cache_file, 'w') as f:
            json.dump(self.__dict__, f)

    def load(self):
        '''Load project cache.'''
        with open(self.cache_file, 'r') as f:
            self.__dict__.update(json.load(f))

    def load_model(self):
        '''Return project model.'''
        spec = importlib.util.spec_from_file_location(self.model_file.stem, self.model_file)
        model = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(model)
        return model

    def kill(self, signal):
        '''Send signal to project.'''
        if signal == 'update':
            # udpate project progress
            if self.status == 'running':
                self.progress += 1
                if self.progress == self.n_trial:
                    self.status = 'done'
            else:
                raise RuntimeError(f'Project (id={self.pid}) is not running.')
        elif signal == 'start':
            # start running a project
            if self.status == 'pending':
                self.status = 'running'
            elif self.status == 'running':
                print(f'Project {self.pid} is already running!')
            else:
                raise RuntimeError(f'Project {self.pid} cannot start.')
        elif signal == 'kill':
            # terminate a project
            self.status = 'killed'
        else:
            raise ValueError('Unknown signal.')


def header_footer_loop(func):
    '''Decorator tha includes header, footer and trial loop for projects.'''
    def wrapper(project, pcache):
        # header
        print(f'\n=================== Trial Start ====================')
        print(f'\t\tProject ID: {pcache.pid}')
        print(f'----------------------------------------------------')

        # signal project to start
        pcache.kill('start')

        # load the model
        model = pcache.load_model()

        # trial loop
        while (pcache.progress < pcache.n_trial):
            print(f'\n[trial {pcache.progress+1}/{pcache.n_trial}]')
            func(project, pcache, model)
        
        # footer
        print('\n=================== Trial End ======================\n')
    return wrapper


@header_footer_loop
def search_parameter(project, pcache, model):
    '''Parameter search and evaluation.'''
    # wait for back-end processing
    sleep(2)

    # request hyper-parameters from DrOpt
    sugt = project.suggestions().create()
    sugt_id = sugt.suggest_id
    sugt_value = sugt.assignments
    print(f'Suggestion = {sugt_value}')

    # evaluate the model with the suggested parameter configuration
    params = pcache.model_params.copy()
    params.update(sugt_value)
    try:
        metric = model.run(params)
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
        pid    - id of the selected project
    '''

    # read resume files
    choices = []
    for f in PCACHE_DIR.glob('*'):
        with open(f) as fh:
            pcache_dict = json.load(fh)
        if pcache_dict['status'] != 'running':
            continue
        pid = pcache_dict['pid']
        name = pcache_dict['name']
        n_trial = pcache_dict['n_trial']
        progress = pcache_dict['progress']
        create_time = pcache_dict['create_time']
        choices.append(questionary.Choice(
            title=f'[Project {pid}: {name}] progress: {progress}/{n_trial} (created at {create_time})',
            value=int(pid)
        ))
        
    if len(choices) == 0:
        print("There are no running projects!")
        sys.exit(1)
        
    return questionary.select(
               "Which project would you like to resume?",
               choices = choices
           ).ask()
