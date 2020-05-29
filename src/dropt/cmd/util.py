import questionary
from dropt.client.util import is_int
import os
import sys
import ctypes
import json
import time
from pathlib import Path

class ProjectCache:
    '''Project cache.'''
    def __init__(self, project_id, config, create_time=time, progress=0, status='pending', path='.dropt/projects'):
        # create directory if it does not exist
        path = Path(path)
        try:
            path.mkdir(parent=True, exist_ok=True)
        except FileExistsError as e:
            print('Directory path conflicts with an existing regular file: {e}')
            sys.exit(1)

        self.filename = path.joinpath(filename)
        self.project_id = project_id
        self.write()

    def write(self):
        with open(self.filename, 'w') as f:
            json.dump(self.data, f)

    def read(self):
        with open(self.filename, 'r') as f:
            self.data = json.load(f)

    def update(self):
        self.data['progress'] += 1

    def close(self)


def write_project_cache(filename, data):
    filename = PROJECTS_DIR.joinpath(filename)
    with open(filename, 'w')


def update_project_cache(filename, status=None):
    """ 
    Update the progress of a project progress file. 
    (Default action: progress += 1. The status is used to update the project status (e.g. running or done)
    """

    # TODO: if the progress file does not exist, create it

    project_log['progress'] += 1

    # read config file
    with open(os.path.join(PROGRESS_DIR, f'.{file_name}.json'), 'r') as f:
        data = json.load(f)
    data['progress'] += 1
    if status == 'done':
        data['status'] = 'done'
    with open(os.path.join(PROGRESS_DIR, f'.{file_name}.json'), 'w') as f:
        json.dump(data, f)


def resume_prompt():
    """
    Get the resume project_id. 
    Users can select from exist progress files or input the project_id manually.

    Returns:
        project_id    - id of the selected project
        file_progress - progress of the selected local file
    """

    def get_proj_id_input():
        if(questionary.confirm("Would you like to specify a project_id?").ask()):
            proj_id = questionary.text("The project_id you would like to resume:").ask()
            if is_int(proj_id) != True:
                print("\nThe project_id must be an integer! droptctl exited.")
                exit(0)
        else:
            print("\ndroptctl exited.")
            exit(0)
        return proj_id

    # read resume files
    if (os.path.isdir(PROGRESS_DIR) != True):
        print("\n! The project history directory does not exist.\n")
        proj_id = int(get_proj_id_input())
        return proj_id
    elif (len(os.listdir(PROGRESS_DIR)) == 0):
        print("\n! There does not exist any project history file.\n")
        proj_id = int(get_proj_id_input())
        return proj_id
    else:
        project_files = []
        for f in os.listdir(PROGRESS_DIR):
            with open(os.path.join(PROGRESS_DIR, f)) as json_file:
                project_files.append(json.load(json_file)) 
        project_files = sorted(project_files, key=lambda k: k['create_time'], reverse=True) 
        choices =  [ f"[project {p['project_id']}] name: {p['name']}, progress: {p['progress']+1}, create_time: {p['create_time']}"\
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

        return int(user_answer.split(']')[0].split('project ')[1]), int(user_answer.split('progress: ')[1].split(', create_time')[0])
