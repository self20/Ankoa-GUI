#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import subprocess


# MOUNT SOURCE FOLDER
def mount_source_folder():

    mount = 'echo {0} | sshfs {1}@{2}:{3} {4} -C -p '\
            '{5} -o workaround=rename -o password_stdin'\
            .format(ssh_passwd, ssh_username, ssh_host,
                      source_folder, local_folder, ssh_port)
    return session


# UMOUNT SOURCE FOLDER
def umount_source_folder():

    session = 'fusermount -u {}'.format(local_folder)
    return session


# RUN SESSION
def run_sshfs():

    try:
        subprocess.check_output(session, shell=True)

    except OSError as e:
        print (e)
        sys.exit()

    except subprocess.CalledProcessError as e:
        print (e)
        sys.exit()
