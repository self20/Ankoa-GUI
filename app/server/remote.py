#!/usr/bin/kivy
import sys
import subprocess
from app.settings.conf_dict import session


# Session control
def remote(request):
    ''' Mount & umount remote folder to local
    on demand, using sshfs and fusermount '''

    # Mount source folder cmd
    if request == 'mount_source_folder':
        session = 'echo {0} | sshfs {1}@{2}:{3} {4} -C -p '\
                  '{5} -o workaround=rename -o password_stdin'\
                  .format(session['ssh_passwd'], session['ssh_username'],
                          session['ssh_host'], session['remote_folder'],
                          session['source_folder'], session['ssh_port'])

    # Umount source folder cmd
    elif request == 'umount_source_folder':
        session = 'fusermount -u {}'.format(session['source_folder'])

    # Run requested action & restart
    try:
        subprocess.call(session)

    except OSError as e:
        print (e)
        sys.exit()
    except subprocess.CalledProcessError as e:
        print (e)
        sys.exit()
