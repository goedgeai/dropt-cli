'''DrOpt controller.

This is the DrOpt project control script.
It encapsulates the procedure for creating and running a DrOpt project
by standardizing the required model file and the config file.

Usage:
  Run command under the directory storing your DrOpt
  project (which typically includes 'model.py' and 'config.json'):

    $ droptctl CMD [options]

  Use option [-h] to learn the detail.
'''


from dropt.client.interface import Connection
from .launcher import create_project, resume_project
from pkg_resources import get_distribution
import argparse
import sys


def start():
    '''droptctl command parser.'''
    parser = argparse.ArgumentParser(prog='droptctl',
                                     description='Use command to control DrOpt project.',
                                     epilog='Run "droptctl CMD -h" to learn more about a specific command.')
    parser.add_argument('-v', '--version', action='version', version=get_distribution('dropt-cli').version)
    parser.add_argument('-t', '--token', help='user token', required=True)
    parser.add_argument('-s', '--server', metavar='ADDRESS',
                        default='dropt.neuralscope.org',
                        help='server address (default: %(default)s)')
    parser.add_argument('-p', '--port',
                        default='',
                        help='port number')

    # create subparesers for commands
    subparsers = parser.add_subparsers(title='commands', metavar='CMD')

    # command 'create': create a new project
    parser_create = subparsers.add_parser('create', help='create new project',
                                          description='Create new DrOpt project.')
    parser_create.add_argument('-c', '--config-file', metavar='FILENAME',
                               default='config.json',
                               help='config file (default: %(default)s)')
    parser_create.set_defaults(func=create_project)

    # command 'resume': resume a existing project
    parser_resume = subparsers.add_parser('resume', help='resume an existing project',
                                          description='Create new DrOpt project.')
    parser_resume.set_defaults(func=resume_project)

    # show help info if no argument is given
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    # parse arguments
    args, _ = parser.parse_known_args()
    kwargs = vars(args)

    # establish connection
    kwargs['conn'] = Connection(client_token=kwargs.pop('token'),
                                server_ip=kwargs.pop('server'),
                                server_port=kwargs.pop('port'))

    # run the associated function
    func = kwargs.pop('func')
    func(**kwargs)


if __name__ == '__main__':
    start()
