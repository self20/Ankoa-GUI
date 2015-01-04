#!/usr/bin/kivy
''' [ GLOBAL SETTINGS DICTIONARIES ]
    user > user settings
    session > user session
    filter > filemanager filters
    error > errors messages
'''

user = {

    'source_folder': '',
    'dest_folder': '',
    'team_name': '',
    'tmdb_apikey': '',
    'tk_announce': ''
}

session = {

    'ssh_host': '',
    'ssh_port': '',
    'ssh_username': '',
    'ssh_passwd': '',
    'local_folder': '',
    'remote_folder': ''
}

filter = {

    'request': '',
    'folder_type': '',

    'folder': ['!*.*'],

    'encode_source': ['*.mp4', '*.mkv', '*.h264',
                      '*.m2ts', '.iso', '*.img', '*.h265'],

    'remux_source': ['*.mkv', '*.mp4'],

    'extract_source': ['*.mp4', '*.mkv',
                       '*.m2ts', '.iso', '*.img'],

    'sub_source': ['*.ass', '*.srt', '*.vobsub', '*.pgs'],

    'audio_source': ['*.ac3', '*.acc', '*.mp3', '*.dts']
}

error = {
    'missing': 'Some values are missing !',
    'reset': 'Session settings are not defined !',
    'umount': 'No drive mounted !',
    'settings': 'User settings are not defined !',

    'source': 'No release source selected !',
    'title': 'Please specify release title !',
    'reso': 'Video resolution not specified !',
    'video': 'Specify valid video track ID !',
    'codec': 'Specify video codec output !'
}
