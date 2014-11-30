#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
from subprocess import getoutput


# SCAN SOURCE
def scan_source(source):

    try:
        scan_media = os.popen('mediainfo {}'.format(source))
        mediainfo = scan_media.read()
        scan_media.close()

        scan_HB = getoutput('HandBrakeCLI -t 0 --scan -i {}'
                            .format(source))

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
