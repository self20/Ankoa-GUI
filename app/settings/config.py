#!/usr/bin/kivy
import os
import configparser
from app.settings.conf_dict import (user, session)

# Create config object
conf = configparser.ConfigParser()

# Set .cfg filenames and sections
conf_file = ['user/settings.cfg', 'user/session.cfg']
section = ['USER_SETTINGS', 'USER_SESSION']


# Load settings
def load_settings():

    # Check if settings file exists and not empty
    if os.path.exists(conf_file[0]) is True and\
            os.path.getsize(conf_file[0]) > 0:

        # Read settings file
        conf.read(conf_file[0])

        # Load defined settings
        user['source_folder'] = conf.get(section[0], 'source_folder')
        user['dest_folder'] = conf.get(section[0], 'dest_folder')
        user['team_name'] = conf.get(section[0], 'team_name')
        user['tmdb_apikey'] = conf.get(section[0], 'tmdb_apikey')
        user['tk_announce'] = conf.get(section[0], 'tk_announce')


# Load session
def load_session():

    # Check if session exists and not empty
    if os.path.exists(conf_file[1]) is True and\
            os.path.getsize(conf_file[1]) > 0:

        # Load session file
        conf.read(conf_file[1])

        # Load defined session
        session['ssh_host'] = conf.get(section[1], 'ssh_host')
        session['ssh_port'] = conf.get(section[1], 'ssh_port')
        session['ssh_username'] = conf.get(section[1], 'ssh_username')
        session['ssh_passwd'] = conf.get(section[1], 'ssh_passwd')
        session['local_folder'] = conf.get(section[1], 'local_folder')
        session['remote_folder'] = conf.get(section[1], 'remote_folder')


# Save settings
def modify_settings():

    # Set section if file doesn't exists or empty
    if os.path.exists(conf_file[0]) is False or\
            os.path.getsize(conf_file[0]) == 0:
        conf.add_section(section[0])

    # Set defined settings
    conf.set(section[0], 'source_folder', user['source_folder'])
    conf.set(section[0], 'dest_folder', user['dest_folder'])
    conf.set(section[0], 'team_name', user['team_name'])
    conf.set(section[0], 'tmdb_apikey', user['tmdb_apikey'])
    conf.set(section[0], 'tk_announce', user['tk_announce'])

    # Write settings file
    conf.write(open(conf_file[0], 'w'))


# Save session
def modify_session():

    # Set section if file doesn't exists or empty
    if os.path.exists(conf_file[1]) is False or\
            os.path.getsize(conf_file[1]) == 0:
        conf.add_section(section[1])

    # Set defined session
    conf.set(section[1], 'ssh_host', session['ssh_host'])
    conf.set(section[1], 'ssh_port', session['ssh_port'])
    conf.set(section[1], 'ssh_username', session['ssh_username'])
    conf.set(section[1], 'ssh_passwd', session['ssh_passwd'])
    conf.set(section[1], 'remote_folder', session['remote_folder'])
    conf.set(section[1], 'local_folder', session['local_folder'])

    # Write session file
    conf.write(open(conf_file[1], 'w'))


# Clear settings
def clear_settings():

    # Remove settings and write conf file if exists
    if os.path.exists(conf_file[0]) is True:
        conf.remove_section(section[0])
        conf.write(open(conf_file[0], 'w'))


# Clear session
def clear_session():

    # Remove session and write conf file if exists
    if os.path.exists(conf_file[1]) is True:
        conf.remove_section(section[1])
        conf.write(open(conf_file[1], 'w'))
