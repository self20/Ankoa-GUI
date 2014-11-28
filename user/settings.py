#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import configparser

conf = configparser.ConfigParser()


# LOAD USER SETTINGS
def load_settings():

    if os.path.exists('user/user.cfg') is True:
        conf.read('user/user.cfg')

        source_folder = conf.get('USER_SETTINGS', 'source_folder')
        dest_folder = conf.get('USER_SETTINGS', 'dest_folder')
        team_name = conf.get('USER_SETTINGS', 'team_name')
        tmdb_apikey = conf.get('USER_SETTINGS', 'tmdb_apikey')
        tk_announce = conf.get('USER_SETTINGS', 'tk_announce')
        ssh_host = conf.get('USER_SETTINGS', 'ssh_host')
        ssh_port = conf.get('USER_SETTINGS', 'ssh_port')
        ssh_username = conf.get('USER_SETTINGS', 'ssh_username')
        ssh_passwd = conf.get('USER_SETTINGS', 'ssh_passwd')
        local_folder = conf.get('USER_SETTINGS', 'local_folder')

    else:
        [source_folder, dest_folder, team_name,
         tmdb_apikey, tk_announce, ssh_host, ssh_port,
         ssh_username, ssh_passwd, local_folder] = ['', ] * 10

    return (source_folder, dest_folder, team_name,
            tmdb_apikey, tk_announce, ssh_host, ssh_port,
            ssh_username, ssh_passwd, local_folder)

# SAVE USER SETTINGS
def modify_settings(source_folder, dest_folder, team_name,
                    tmdb_apikey, tk_announce, ssh_host, ssh_port,
                    ssh_username, ssh_passwd, local_folder):

    if os.path.exists('user/user.cfg') is False:
        conf.add_section('USER_SETTINGS')

    conf.set('USER_SETTINGS', 'source_folder', source_folder)
    conf.set('USER_SETTINGS', 'dest_folder', dest_folder)
    conf.set('USER_SETTINGS', 'team_name', team_name)
    conf.set('USER_SETTINGS', 'tmdb_apikey', tmdb_apikey)
    conf.set('USER_SETTINGS', 'tk_announce', tk_announce)
    conf.set('USER_SETTINGS', 'ssh_host', ssh_host)
    conf.set('USER_SETTINGS', 'ssh_port', ssh_port)
    conf.set('USER_SETTINGS', 'ssh_username', ssh_username)
    conf.set('USER_SETTINGS', 'ssh_passwd', ssh_passwd)
    conf.set('USER_SETTINGS', 'local_folder', local_folder)

    conf.write(open('user/user.cfg','w'))


# CLEAR USER SETTINGS
def clear_settings():

    if os.path.exists('user/user.cfg') is True:
        conf.remove_section('USER_SETTINGS')
        conf.write(open('user/user.cfg','w'))
