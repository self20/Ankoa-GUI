#!/usr/bin/kivy


# Video bitrate calculator
def calculator(HH, MM, SS, audio_bit, desired_size):
    '''
    Calculate required video bitrate by specify
    Video duration, audio bitrate and desired size
    '''

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
