from .util import ProjectCache, search_parameter
import questionary
from dropt.client.util import is_int
import json
import time
import os


def create_project(conn, config_file):
    """Create and run a DrOpt project."""
    # load config file
    with open(config_file, 'r') as f:
        config = json.load(f)

    # create a new project and its cache
    project = conn.projects().create(config=config)
    pcache = ProjectCache(project_id=project.project_id, n_trial=project.trial, config=config)
    project = conn.projects(pcache.project_id)

    # search parameter
    search_parameter(project, pcache)


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
