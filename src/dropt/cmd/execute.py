import os
import ctypes
import json
import time

import questionary

from dropt.client.util import is_int

FILE_ATTRIBUTE_HIDDEN = 0x02
PROGRESS_DIR = '.progress'

project_log = {"project_id": None, "name": None, "progress": 0, "config": None, "create_time": None, "status": "running"}

def write_progress_file(file_name, data):
    """
    Create a hidden dir ".progress" in the current dir (if it does not exist), 
    and write the project progress file according to the project id.
    """

    # This function is modified from: https://stackoverflow.com/questions/25432139/python-cross-platform-hidden-file
    
    # For *nix add a '.' prefix
    prefix = '.' if os.name != 'nt' else ''
    file_name = prefix + file_name

    # If no .progress dir, create it
    if (os.path.isdir(PROGRESS_DIR) != True):
        try:
            os.mkdir(PROGRESS_DIR)
        except Exception as e:
            print(f"! Failed to create progress dir: {e}\n")
            if (questionary.confirm("Would you like to continue the project? (If resuming project is needed, please record the project_id)").ask() == False):
                print("droptctl exited.")
                exit(0)

    # Write file
    with open(os.path.join(PROGRESS_DIR, file_name+'.json'), 'w') as f:
        json.dump(data, f)

    # For windows set file attribute
    if os.name == 'nt':
        ret = ctypes.windll.kernel32.SetFileAttributesW(file_name, FILE_ATTRIBUTE_HIDDEN)
        if not ret: # There was an error
            raise ctypes.WinError()

def update_progress_file(file_name, status=None):
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

def create_project(cmd, conn, conf):
    """ Create and return a Dr.Opt project. """
    if cmd != 'create':
        return (None, None, None, None)
    project = conn.projects().create(config=json.dumps(conf))
    pid = project.project_id
    n_trial = project.trial
    project = conn.projects(pid)
    project_log['project_id'] = pid
    project_log['config'] = conf
    project_log['name'] = conf.get('config').get('experimentName')
    project_log['create_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    write_progress_file(str(pid), project_log)

    # pid, trial_num, progress, project
    return (pid, n_trial, 0, project)

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

def resume_project(cmd, conn):
    """ Create a resume request and return the project object. """
    if cmd != 'resume':
        return (None, None, None, None)
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

def execute_cmd(cmd, conn, conf=None):
    """
    Execute the given droptctl command.

    Parameters:
        cmd  - the command specified by the user (e.g. create, resume, etc.)
        conn - a Connecntion object (defined in client/interface)
        conf - project configuration (used when creating a project)

    Returns:
        porject_id, n_trial, progress, project

    Raises:
        KeyError - if the command is unknown, raise an exception
    """

    cmd_list = ['create', 'resume']

    if cmd not in cmd_list:
        raise KeyError(f"droptctl: unknown command '{cmd}'! Available commands are: {cmd_list}")
    
    return {
        'create': create_project(cmd, conn, conf),
        'resume': resume_project(cmd, conn)
    }.get(cmd, 'not_found')


