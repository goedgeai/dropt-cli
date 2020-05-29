import ctypes
import questionary
from dropt.client.util import is_int
import json
import time
import os


FILE_ATTRIBUTE_HIDDEN = 0x02
PROGRESS_DIR = '.progress'

project_log = {"project_id": None, "name": None, "progress": 0, "config": None, "create_time": None, "status": "running"}


def header_footer_loop(func):
    '''Decorator tha includes header, footer and trial loop for projects.'''
    def wrapper(project, model, params, pid, n_trial, progress):
        # header
        print(f'\n=================== Trial Start ====================')
        print(f'\t\tProject ID: {pid}')
        print(f'----------------------------------------------------')

        # trial loop
        for i in range(progress, n_trial):
            print(f'\n[trial {i+1}/{n_trial}]')
            func(project, model, params)
        
        # save project log
        # project_log['status'] = 'done'
        update_progress_file(project_log['project_id'], 'done')
        
        # footer
        print('\n=================== Trial End ======================\n')
    return wrapper


@header_footer_loop
def search_parameter(project, model, params):
    '''Parameter search and evaluation.'''
    # wait for back-end processing
    sleep(2)

    # request hyper-parameters from DrOpt
    sugt = project.suggestions().create()
    sugt_id = sugt.suggest_id
    sugt_value = sugt.assignments

    # evaluate the model with the suggested parameter configuration
    params.update(sugt_value)
    print(f"Suggestion = {sugt_value}")
    try:
        metric = model.run(params)
    except RuntimeError as exc:
        print(exc)
        print('Please add RuntimeError handler in your model code.')
        sys.exit(1)
    print(f"Evaluation: {metric}")

    # report result to DrOpt
    project.validations().create(suggest_id=sugt_id, value=metric)

    # update project_log
    update_progress_file(project_log['project_id'])


def create_project(conn, config_file):
    """Create and run a DrOpt project."""
    # create a new project
    project = conn.projects().create(config=json.dumps(conf))
    pid = project.project_id
    n_trial = project.trial
    project = conn.projects(pid)

    status = dict()
    project_cache['project_id'] = pid
    project_cache['config'] = conf
    project_cache['name'] = conf.get('config').get('experimentName')
    project_cache['create_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    write_progress_file(str(pid), project_log)

    # pid, trial_num, progress, project
    return (pid, n_trial, 0, project)


def resume_project(conn):
    """ Create a resume request and return the project object. """
    # read config file
    with open(args.config, 'r') as file:
        conf = json.load(file)

    # find project id
    project_id, file_progress = resume_prompt()
    project = conn.projects().resume(project_id=project_id)
    pid = project.project_id
    progress = project.progress

    if file_progress != progress and file_progress != progress-1:
        if (questionary.confirm("Local file / server progress mismatches! server progress: {progress}. Would you like to continue?").ask() == False):
                print("droptctl exited.")
                exit(0)

    n_trial = project.trial
    project = conn.projects(pid)
    project_log['project_id'] = pid

    return (pid, n_trial, progress-1, project)
