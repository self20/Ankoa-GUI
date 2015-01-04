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
    if request == 'Mount':
        cmd = 'echo {0} | sshfs {1}@{2}:{3} {4} -C -p '\
              '{5} -o workaround=rename -o password_stdin'\
              .format(session['ssh_passwd'], session['ssh_username'],
                      session['ssh_host'], session['remote_folder'],
                      session['local_folder'], session['ssh_port'])

    # Umount source folder
    elif request == 'Umount':
        cmd = 'fusermount -u {}'.format(session['local_folder'])

    # Run requested action
    try:
        subprocess.call(cmd)

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
