#!/usr/bin/kivy
import os
import sys
import subprocess
from app.settings.conf_dict import user


# Remote session control
def remote(request):
    '''
    Mount & umount remote folder to local on demand
    Usage of sshfs and fusermount
    '''

    # Mount source folder cmd
    if request == 'mount_source_folder':
        session = 'echo {0} | sshfs {1}@{2}:{3} {4} -C -p '\
                  '{5} -o workaround=rename -o password_stdin'\
                  .format(user['ssh_passwd'], user['ssh_username'],
                          user['ssh_host'], user['remote_folder'],
                          user['source_folder'], user['ssh_port'])

    # Umount source folder cmd
    elif request == 'umount_source_folder':
        session = 'fusermount -u {}'.format(user['source_folder'])

    # Run requested action & restart
    if user['ssh_passwd'] or user['ssh_username'] or user['remote_folder']:
        try:
            os.system(session)
            restart = sys.executable
            os.execl(restart, restart, * sys.argv)

        except OSError as e:
            print (e)
            sys.exit()

        # except subprocess.CalledProcessError as e:
        #     print (e)
        #     sys.exit()
