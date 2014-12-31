#!/usr/bin/kivy
import os
import sys
from app.settings.conf_dict import user


# Session control
def remote(request):
    ''' Mount & umount remote folder to local
    on demand, using sshfs and fusermount '''

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
    if user['usage'] == 'remote_usage':
        try:
            os.system(session)
            restart = sys.executable
            os.execl(restart, restart, * sys.argv)

        except OSError as e:
            print (e)
            sys.exit()
