#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import subprocess


# REMOTE CONTROL
def remote(request, ssh_passwd, ssh_username, ssh_host,
           source_folder, remote_folder, ssh_port):

    if request == 'mount_source_folder':
        session = 'echo {0} | sshfs {1}@{2}:{3} {4} -C -p '\
                  '{5} -o workaround=rename -o password_stdin'\
                  .format(ssh_passwd, ssh_username, ssh_host,
                          remote_folder, source_folder, ssh_port)

    elif request == 'umount_source_folder':
        session = 'fusermount -u {}'.format(source_folder)

    if ssh_passwd == '' or ssh_username == '' or remote_folder == '':
        pass
    else:
        try:
            os.system(session)

        except OSError as e:
            print (e)
            sys.exit()

        # except subprocess.CalledProcessError as e:
        #     print (e)
        #     sys.exit()
