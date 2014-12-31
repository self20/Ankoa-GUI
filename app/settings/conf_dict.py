#!/usr/bin/kivy
''' [ USER SETTINGS ]
Dictionary to manage user settings '''

user = {

    # Settings
    'usage': '',
    'source_folder': '',
    'dest_folder': '',
    'team_name': '',
    'tmdb_apikey': '',
    'tk_announce': '',
    'ssh_host': '',
    'ssh_port': '',
    'ssh_username': '',
    'ssh_passwd': '',
    'remote_folder': '',

    # Filters
    'request': '',

    'encode_filter': ['*.mp4', '*.mkv', '*.h264',
                      '*.m2ts', '.iso', '*.img', '*.h265'],

    'remux_filter': ['*.mkv', '*.mp4'],

    'extract_filter': ['*.mp4', '*.mkv',
                       '*.m2ts', '.iso', '*.img'],

    'sub_filter': ['*.ass', '*.srt', '*.vobsub', '*.pgs'],

    'audio_filter': ['*.ac3', '*.acc', '*.mp3', '*.dts']
}
