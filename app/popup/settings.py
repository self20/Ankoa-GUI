#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import configparser

conf = configparser.ConfigParser()
conf_file = 'user/settings.cfg'
section = 'USER_SETTINGS'


# LOAD USER SETTINGS
def load_settings():

    if os.path.exists(conf_file) is True and\
            os.path.getsize(conf_file) > 0:
        conf.read(conf_file)

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

    else:
        [source_folder, dest_folder, team_name,
         tmdb_apikey, tk_announce, ssh_host, ssh_port,
         ssh_username, ssh_passwd, remote_folder] = ['', ] * 10

    return (source_folder, dest_folder, team_name,
            tmdb_apikey, tk_announce, ssh_host, ssh_port,
            ssh_username, ssh_passwd, remote_folder)


# SAVE USER SETTINGS
def modify_settings(source_folder, dest_folder, team_name,
                    tmdb_apikey, tk_announce, ssh_host, ssh_port,
                    ssh_username, ssh_passwd, remote_folder):

    if os.path.exists(conf_file) is False or\
            os.path.getsize(conf_file) == 0:
        conf.add_section(section)

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

    conf.write(open(conf_file,'w'))


# CLEAR USER SETTINGS
def clear_settings():

    if os.path.exists(conf_file) is True:
        conf.remove_section(section)
        conf.write(open(conf_file,'w'))
