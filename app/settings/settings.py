#!/usr/bin/kivy
import os
import configparser

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
        source_folder = conf.get(section, 'source_folder')
        dest_folder = conf.get(section, 'dest_folder')
        team_name = conf.get(section, 'team_name')
        tmdb_apikey = conf.get(section, 'tmdb_apikey')
        tk_announce = conf.get(section, 'tk_announce')
        ssh_host = conf.get(section, 'ssh_host')
        ssh_port = conf.get(section, 'ssh_port')
        ssh_username = conf.get(section, 'ssh_username')
        ssh_passwd = conf.get(section, 'ssh_passwd')
        remote_folder = conf.get(section, 'remote_folder')

    # Set empty variables when conf file is empty
    else:
        [source_folder, dest_folder, team_name,
         tmdb_apikey, tk_announce, ssh_host, ssh_port,
         ssh_username, ssh_passwd, remote_folder] = ['', ] * 10

    return (source_folder, dest_folder, team_name,
            tmdb_apikey, tk_announce, ssh_host, ssh_port,
            ssh_username, ssh_passwd, remote_folder)


# Save user settings
def modify_settings(source_folder, dest_folder, team_name,
                    tmdb_apikey, tk_announce, ssh_host, ssh_port,
                    ssh_username, ssh_passwd, remote_folder):

    # Set section if conf file exists and empty
    if os.path.exists(conf_file) is False or\
            os.path.getsize(conf_file) == 0:
        conf.add_section(section)

    # Set defined options
    conf.set(section, 'source_folder', source_folder)
    conf.set(section, 'dest_folder', dest_folder)
    conf.set(section, 'team_name', team_name)
    conf.set(section, 'tmdb_apikey', tmdb_apikey)
    conf.set(section, 'tk_announce', tk_announce)
    conf.set(section, 'ssh_host', ssh_host)
    conf.set(section, 'ssh_port', ssh_port)
    conf.set(section, 'ssh_username', ssh_username)
    conf.set(section, 'ssh_passwd', ssh_passwd)
    conf.set(section, 'remote_folder', remote_folder)

    # Write conf file
    conf.write(open(conf_file,'w'))


# Clear user settings
def clear_settings():

    # Remove options and write conf file if exists
    if os.path.exists(conf_file) is True:
        conf.remove_section(section)
        conf.write(open(conf_file,'w'))
