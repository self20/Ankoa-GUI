#!/usr/bin/kivy
from app.mod_encode.encode_dict import u_u


def calculator():
    ''' Calculate required video bitrate by specify
    video duration, audio bitrate and desired size '''

    # Target sizes
    calsize = u_u['bit_sizes'][int(u_u['desired_size'])]

    # Audio bitrates
    audiobit = u_u['audiobit'][int(u_u['audio_bit'])]

    # Formula!
    bitrate = \
        ((float(calsize)-((int(audiobit)/8)/1024*(
            (int(u_u['HH'])*3600) + (int(u_u['MM'])*60)+int(
                u_u['SS']))))/((int(u_u['HH'])*3600)+(
                    int(u_u['MM'])*60)+int(u_u['SS'])))*8*1024

    # Round result to integer
    if int(str(round(bitrate, 2)).split('.')[1]) > 51:
        current_bitrate = int(str(round(bitrate+1, 1)).split('.')[0])
    else:
        current_bitrate = int(str(round(bitrate, 1)).split('.')[0])

    return current_bitrate
