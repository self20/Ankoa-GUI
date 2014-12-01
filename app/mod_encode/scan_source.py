#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from subprocess import getoutput


# SCAN SOURCE
def scan(source):

    try:
        scan_MI = getoutput('mediainfo {}'.format(source))

        scan_HB = getoutput('HandBrakeCLI -t 0 --scan -i {}'
                            .format(source))

        mediainfo = ''.join(scan_MI)

        HB_data = scan_HB.splitlines()
        [ar_infos, autocrop] = ['', ] * 2
        for line in HB_data:
            if 'autocrop' in line and 'aspect' in line:
                ar_infos = line
            elif '+ autocrop' in line:
                autocrop = line.replace('+', '')

        scan_data = '{0}\n\n{1}\n\n{2}'.format(ar_infos.strip(),
                                               mediainfo.strip(),
                                               autocrop.strip())
        return scan_data

    except OSError as e:
        print (e)
        sys.exit()
