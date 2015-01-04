#!/usr/bin/kivy
import configparser
from app.settings.conf_dict import (user, session)

# Configparser object
conf = configparser.ConfigParser()
conf_file = 'user/settings.cfg'
section = ['USER_SETTINGS', 'USER_SESSION']
conf.read(conf_file)


# Load settings
def load_settings():

    # Complete user dictionary
    if conf.has_section(section[0]) is True:
        user['source_folder'] = conf.get(section[0], 'source_folder')
        user['dest_folder'] = conf.get(section[0], 'dest_folder')
        user['team_name'] = conf.get(section[0], 'team_name')
        user['tmdb_apikey'] = conf.get(section[0], 'tmdb_apikey')
        user['tk_announce'] = conf.get(section[0], 'tk_announce')


# Load session
def load_session():

    # Complete session dictionary
    if  conf.has_section(section[1]) is True:
        session['ssh_host'] = conf.get(section[1], 'ssh_host')
        session['ssh_port'] = conf.get(section[1], 'ssh_port')
        session['ssh_username'] = conf.get(section[1], 'ssh_username')
        session['ssh_passwd'] = conf.get(section[1], 'ssh_passwd')
        session['local_folder'] = conf.get(section[1], 'local_folder')
        session['remote_folder'] = conf.get(section[1], 'remote_folder')


# Save settings
def modify_settings(current):

    # Set dictionary
    user['source_folder'] = current.ids.source_folder.text
    user['dest_folder'] = current.ids.dest_folder.text
    user['team_name'] = current.ids.team_name.text
    user['tmdb_apikey'] = current.ids.tmdb_apikey.text
    user['tk_announce'] = current.ids.tk_announce.text

    # Set section
    if conf.has_section(section[0]) is False:
        conf.add_section(section[0])

    # Set settings
    conf.set(section[0], 'source_folder', user['source_folder'])
    conf.set(section[0], 'dest_folder', user['dest_folder'])
    conf.set(section[0], 'team_name', user['team_name'])
    conf.set(section[0], 'tmdb_apikey', user['tmdb_apikey'])
    conf.set(section[0], 'tk_announce', user['tk_announce'])

    # Write settings
    conf.write(open(conf_file, 'w'))


# Save session
def modify_session(current):

    # Set dictionary
    session['ssh_host'] = current.ids.ssh_host.text
    session['ssh_port'] = current.ids.ssh_port.text
    session['ssh_username'] = current.ids.ssh_username.text
    session['ssh_passwd'] = current.ids.ssh_passwd.text
    session['remote_folder'] = current.ids.remote_folder.text
    session['local_folder'] = current.ids.local_folder.text

    # Set section
    if conf.has_section(section[1]) is False:
        conf.add_section(section[1])

    # Set session
    conf.set(section[1], 'ssh_host', session['ssh_host'])
    conf.set(section[1], 'ssh_port', session['ssh_port'])
    conf.set(section[1], 'ssh_username', session['ssh_username'])
    conf.set(section[1], 'ssh_passwd', session['ssh_passwd'])
    conf.set(section[1], 'remote_folder', session['remote_folder'])
    conf.set(section[1], 'local_folder', session['local_folder'])

    # Write session
    conf.write(open(conf_file, 'w'))


# Clear settings
def clear_settings(current):

    # Clear popup
    [current.ids.source_folder.text, current.ids.dest_folder.text,
     current.ids.team_name.text, current.ids.tmdb_apikey.text,
     current.ids.tk_announce.text] = ['', ] * 5

    # Clear Dictionary
    for key, value in user.items():
        if isinstance(value, list):
            user[key] = []
        else:
            user[key] = ''

    # Clear settings
    if conf.has_section(section[0]) is True:
        conf.remove_section(section[0])
        conf.write(open(conf_file, 'w'))


# Clear session
def clear_session(current):

    # Clear popup
    [current.ids.ssh_host.text, current.ids.ssh_port.text,
     current.ids.ssh_username.text, current.ids.ssh_passwd.text,
     current.ids.remote_folder.text,
     current.ids.local_folder.text] = ['', ] * 6

    # Clear Dictionary
    for key, value in session.items():
        if isinstance(value, list):
            session[key] = []
        else:
            session[key] = ''

    # Clear settings
    if conf.has_section(section[1]) is True:
        conf.remove_section(section[1])
        conf.write(open(conf_file, 'w'))
