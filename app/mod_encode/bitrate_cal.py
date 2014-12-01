#!/usr/bin/python
# -*- coding: utf-8 -*-
import re


# Video bitrate calculator
def calculator(HH, MM, SS, audio_bit, desired_size):
    '''
        Calculate required video bitrate by specify
        video duration, audio bitrate and desired size
    '''

    # Duration: HOURS
    verif_HH = re.compile(r'^[0].+', flags=0).search(HH)
    while not HH or HH.isdigit() is False\
            or verif_HH is not None or int(HH) > 23:
        pass # todo: add popup error

    # Duration: MINUTES
    verif_MM = re.compile(r'^[0].+', flags=0).search(MM)
    while not HH or HH.isdigit() is False\
            or verif_HH is not None or int(HH) > 59:
        pass # todo: add popup error

    # Duration: SECONDS
    verif_SS = re.compile(r'^[0].+', flags=0).search(SS)
    while not HH or HH.isdigit() is False\
            or verif_HH is not None or int(HH) > 23:
        pass # todo: add popup error

    # Target sizes
    bit_sizes = ['357.8', '562.9', '716.3', '1439.3',
                 '2151', '2875.5', '4585.2', '6881.5']
    calsize = bit_sizes[int(desired_size)]

    # Audio bitrates
    audiobit = ['96', '128', '192', '256', '320',
                '384', '448', '640', '755', '1509']
    audiobit = audiobit[int(audio_bit)]

    # Formula
    bitrate = \
        ((float(calsize)-((int(audiobit)/8)/1024*((int(HH)*3600)\
        +(int(MM)*60)+int(SS))))/((int(HH)*3600)+(int(MM)*60)\
        +int(SS)))*8*1024

    # Round result to integer
    if int(str(round(bitrate, 2)).split('.')[1]) > 51:
        current_bitrate = int(str(round(bitrate+1, 1)).split('.')[0])
    else:
        current_bitrate = int(str(round(bitrate, 1)).split('.')[0])

    return current_bitrate
