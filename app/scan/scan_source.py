#!/usr/bin/kivy
import sys
import platform
import subprocess


# Scan source infos
def scan(source):
    ''' Scan video source to get required informations
    Return complete mediainfo and HandBrake autocrop '''
    try:

        # Windows users
        if 'Windows' in platform.system():
            scan_MI = subprocess.check_output(
                'contrib\mediainfo\MediaInfo.exe {}'.format(source))
            mediainfo = '{}'.format(
                scan_MI.decode('utf-8').replace('\r', ''))
            scan_HB = subprocess.check_output(
                'contrib\handbrake\HandBrakeCLI.exe'
                ' -t 0 --scan -i {}'.format(source),
                stderr=subprocess.STDOUT, shell=True)
            handbrake = '{}'.format(
                scan_HB.decode('utf-8').replace('\r', ''))
            HB_data = handbrake.splitlines()

        # Unix users
        elif 'Linux' in platform.system():
            scan_MI = subprocess.getoutput(
                'contrib/mediainfo/MediaInfo_unix {}'.format(source))
            mediainfo = ''.join(scan_MI)
            scan_HB = subprocess.getoutput(
                'contrib/handbrake/HandBrakeCLI_unix -t 0'
                ' --scan -i {}'.format(source))
            HB_data = scan_HB.splitlines()

        # Get autocrop & duration
        [ar_infos, autocrop, duration] = ['', ] * 3
        for line in HB_data:
            if 'autocrop' in line and 'aspect' in line:
                ar_infos = line.split('] ')[-1]
            if '+ autocrop' in line:
                autocrop = line.replace('+', '')
            if 'duration' in line:
                duration = line.split(',')[-1]

        # Return HB & mediainfo parsed results
        scan_data = '{0}\n{3}\n{1}\n\n{2}\n\n{1}\n{3}\n{0}'\
                    .format(ar_infos.strip(), duration.strip(),
                            mediainfo.strip(), autocrop.strip())
        return scan_data

    except OSError as e:
        print (e)
        sys.exit()
    except subprocess.CalledProcessError as e:
        print (e)
        sys.exit()
