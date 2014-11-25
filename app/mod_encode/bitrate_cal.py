#!/usr/bin/python
# -*- coding: utf-8 -*-
import re


def calculator(HH, MM, SS, audio_bit, desired_size):

    # HOURS
    verif_HH = re.compile(r'^[0].+', flags=0).search(HH)
    while not HH or HH.isdigit() is False\
            or verif_HH is not None or int(HH) > 23:
        pass # todo: add popup error

    # MINUTES
    verif_MM = re.compile(r'^[0].+', flags=0).search(MM)
    while not HH or HH.isdigit() is False\
            or verif_HH is not None or int(HH) > 59:
        pass # todo: add popup error

    # SECONDS
    verif_SS = re.compile(r'^[0].+', flags=0).search(SS)
    while not HH or HH.isdigit() is False\
            or verif_HH is not None or int(HH) > 23:
        pass # todo: add popup error

    # CALCULATOR VALUES
    bit_sizes = ['357.8', '562.9', '716.3', '1439.3',
                 '2151', '2875.5', '4585.2', '6881.5']

    audiobit = ['96', '128', '192', '256', '320',
                '384', '448', '640', '755', '1509']

    # SIZE & AUDIO BITRATE
    audiobit = audiobit[int(audio_bit)]
    calsize = bit_sizes[int(desired_size)]

    # CALCUL
    bitrate = \
        ((float(calsize)-((int(audiobit)/8)/1024*((int(HH)*3600)\
        +(int(MM)*60)+int(SS))))/((int(HH)*3600)+(int(MM)*60)\
        +int(SS)))*8*1024

    # NEED AN INTEGER
    if int(str(round(bitrate, 2)).split('.')[1]) > 51:
        current_bitrate = int(str(round(bitrate+1, 1)).split('.')[0])
    else:
        current_bitrate = int(str(round(bitrate, 1)).split('.')[0])

    return current_bitrate
