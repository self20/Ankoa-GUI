#!/usr/bin/kivy
'''
[ MODE REMUX ]
Dictionaries to manage remux:
    c_o >
    x_x > parameters values
'''

c_o = {

    # Video track
    'video_ID': '',
    'video_title': '',
    'video_flag': '',
    'aspect_ratio': '',
    'resolution': '',
    'crop': '',
    'framerate': '',
    'video_delay': '',
    'video_compression': '',

    # Audio tracks
    'audio_source': [],
    'audio_title': [],
    'audio_lang': [],
    'audio_flag': [],
    'audio_delay': [],
    'audio_compression': [],

    # Subtitles tracks
    'sub_source': [],
    'sub_title': [],
    'sub_lang': [],
    'sub_flag': [],
    'sub_delay': [],
    'sub_charset': [],
    'sub_compression': []
}

x_x = {
    'aspect_ratio': ['', '4/3', '16/9', '1.33', '1.66',
                     '1.78', '1.85', '2.35', '2.40'],

    'framerate': ['', '24p', '25p', '30p', '50p', '50i',
                  '60p', '60i', '24000/1001p', '30000/1001p',
                  '60000/1001i', '60000/1001p']
}
