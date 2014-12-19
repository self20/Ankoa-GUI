#!/usr/bin/kivy
'''
Scan video source to get required informations
Return complete mediainfo and HandBrake autocrop
'''
import sys
import subprocess


# Scan source infos
def scan(source):
    try:

        # Get HB & mediainfo outputs
        scan_MI = subprocess.getoutput('mediainfo {}'.format(source))
        scan_HB = subprocess.getoutput('HandBrakeCLI -t 0 --scan -i {}'
                                       .format(source))

        # Join mediainfo output
        mediainfo = ''.join(scan_MI)

        # Splitlines HB output and get autocrop & duration
        HB_data = scan_HB.splitlines()
        [ar_infos, autocrop] = ['', ] * 2

        for line in HB_data:
            if 'autocrop' in line and 'aspect' in line:
                ar_infos = line
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
