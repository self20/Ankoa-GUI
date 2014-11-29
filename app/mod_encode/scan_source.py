#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
from subprocess import getoutput


# SCAN SOURCE
def scan_source(source):

    try:
        scan_media = os.popen('mediainfo --Output=...y {}'.format(source))
        mediainfo = scan_media.read()
        scan_media.close()

        scan_HB = getoutput('HandBrakeCLI -t 0 --scan -i {}'
                            .format(source))

        HB_data = scan_HB.splitlines()
        autocrop = ''
        for lines in HB_data:
            if 'autocrop' in lines:
                autocrop = lines.replace('+', '').strip()

        scan_data = '{0}\n{1}'.format(autocrop, mediainfo)
        return scan_data

    except OSError as e:
        print (e)
        sys.exit()
