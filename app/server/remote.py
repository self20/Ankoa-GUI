#!/usr/bin/kivy
import sys
import subprocess
from app.popup.popups import popup_error
from app.settings.conf_dict import session


# Unix
def unix_sshfs(request):
    ''' Mount & umount remote folder to local
    on demand, using sshfs and fusermount. '''

    # Mount source folder
    if request == 'mount_source_folder':
        session = 'echo {0} | sshfs {1}@{2}:{3} {4} -C -p '\
                  '{5} -o workaround=rename -o password_stdin'\
                  .format(session['ssh_passwd'], session['ssh_username'],
                          session['ssh_host'], session['remote_folder'],
                          session['source_folder'], session['ssh_port'])

    # Umount source folder
    elif request == 'umount_source_folder':
        session = 'fusermount -u {}'.format(session['source_folder'])

    # Run requested action
    try:
        subprocess.call(session)

    except OSError as error:
        popup_error(error)
    except subprocess.CalledProcessError as error:
        popup_error(error)


# Windows
def win_sshfs():
    ''' Mount & umount remote folder to local
    on demand, using Dokan_sshfs GUI. '''

    try:
        subprocess.call('contrib\sshfs\win\DokanSSHFS.exe')

    except OSError as error:
        popup_error(error)
    except subprocess.CalledProcessError as error:
        popup_error(error)
