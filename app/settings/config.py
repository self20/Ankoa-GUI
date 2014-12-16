#!/usr/bin/kivy
'''
[ USER SETTINGS ]
Settings Manager
'''
import os
import configparser
from app.settings.conf_dict import user

# Create config memory file
conf = configparser.ConfigParser()

# Set .cfg filename and section
conf_file = 'user/settings.cfg'
section = 'USER_SETTINGS'


# Load user settings
def load_settings():

    # Check if conf file exists and not empty
    if os.path.exists(conf_file) is True and\
            os.path.getsize(conf_file) > 0:

        # Load conf file
        conf.read(conf_file)

        # Load defined options
        user['usage'] = conf.get(section, 'usage')
        user['source_folder'] = conf.get(section, 'source_folder')
        user['dest_folder'] = conf.get(section, 'dest_folder')
        user['team_name'] = conf.get(section, 'team_name')
        user['tmdb_apikey'] = conf.get(section, 'tmdb_apikey')
        user['tk_announce'] = conf.get(section, 'tk_announce')
        user['ssh_host'] = conf.get(section, 'ssh_host')
        user['ssh_port'] = conf.get(section, 'ssh_port')
        user['ssh_username'] = conf.get(section, 'ssh_username')
        user['ssh_passwd'] = conf.get(section, 'ssh_passwd')
        user['remote_folder'] = conf.get(section, 'remote_folder')


# Save user settings
def modify_settings():

    # Set section if conf file exists and empty
    if os.path.exists(conf_file) is False or\
            os.path.getsize(conf_file) == 0:
        conf.add_section(section)

    # Set defined options
    conf.set(section, 'usage', user['usage'])
    conf.set(section, 'source_folder', user['source_folder'])
    conf.set(section, 'dest_folder', user['dest_folder'])
    conf.set(section, 'team_name', user['team_name'])
    conf.set(section, 'tmdb_apikey', user['tmdb_apikey'])
    conf.set(section, 'tk_announce', user['tk_announce'])
    conf.set(section, 'ssh_host', user['ssh_host'])
    conf.set(section, 'ssh_port', user['ssh_port'])
    conf.set(section, 'ssh_username', user['ssh_username'])
    conf.set(section, 'ssh_passwd', user['ssh_passwd'])
    conf.set(section, 'remote_folder', user['remote_folder'])

    # Write conf file
    conf.write(open(conf_file, 'w'))


# Clear user settings
def clear_settings():

    # Remove options and write conf file if exists
    if os.path.exists(conf_file) is True:
        conf.remove_section(section)
        conf.write(open(conf_file, 'w'))
