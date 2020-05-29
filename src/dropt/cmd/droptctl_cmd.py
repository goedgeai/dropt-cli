import ctypes
import questionary
from dropt.client.util import is_int
import json
import time
import os


FILE_ATTRIBUTE_HIDDEN = 0x02
PROGRESS_DIR = '.progress'

project_log = {"project_id": None, "name": None, "progress": 0, "config": None, "create_time": None, "status": "running"}


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
