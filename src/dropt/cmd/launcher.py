from .util import ProjectCache, search_parameter, PCACHE_DIR, resume_prompt
import questionary
import json
import sys
import time
from pathlib import Path


def create_project(conn, config_file):
    """Create and run a DrOpt project."""
    # load config file
    with open(config_file, 'r') as f:
        config = json.load(f)

    # create project and project cache
    project = conn.projects().create(config=json.dumps(config))
    pcache = ProjectCache(pid=project.project_id,
                          name=config['config']['experimentName'],
                          n_trial=project.trial,
                          model_file=f"./{config['config']['model']}.py",
                          model_params=config['params'])
    project = conn.projects(project.project_id)

    # search parameter
    search_parameter(project, pcache)


def resume_project(conn):
    """Resume a running project."""
    # find project id
    pid = resume_prompt()
    project = conn.projects().resume(project_id=pid)
    pcache = ProjectCache(pid)
    pcache.load()

    # check if server and client progresses match
    if (project.progress != pcache.progress+1):
        if (questionary.confirm((f'Client and server progresses mismatch! '
                                 f'server progress: {project.progress} '
                                 f'client progress: {pcache.progress}.  '
                                 f'Would you like to continue?')).ask() == False):
            print("droptctl exited.")
            sys.exit(0)

    project = conn.projects(pid)

    # search parameter
    search_parameter(project, pcache)
