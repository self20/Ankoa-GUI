#!/usr/bin/python
# -*- coding: utf-8 -*-

# ENCODE MODE VARIABLES
fixed_size = ['350MiB', '550MiB', '700MiB', '1.37GiB',
              '2.05GiB', '2.74GiB', '4.37GiB', '6.56GiB']
audio_bitrate = ['96Kbps', '128Kbps', '192Kpbs', '256Kbps',
                 '320Kbps', '384Kbps', '448Kbps', '640Kbps']
ar_sd = ['720x540', '720x432', '720x404',
         '720x390', '720x306', '720x300']

ar_720p = ['1280x960', '1280x768', '1280x720',
           '1280x690', '1280x544', '1280x536']

ar_1080p = ['1440x1080', '1800x1080', '1920x1080',
            '1920x1040', '1920x816', '1920x800']

preset = ['UltraFast', 'SuperFast', 'VeryFast', 'Faster', 'Fast',
          'Slow', 'Slower', 'VerySlow', 'Placebo', 'None']

tune = ['Film', 'Animation', 'Grain', 'Still Image', 'PSNR',
        'SSIM', 'Fast Decode', 'None']

profile = ['Auto', 'Baseline', 'Main', 'High']

level = ['1.0', '1.1', '1.2', '1.3', '2.0', '2.1', '2.2',
         '3.0', '3.1', '3.2', '4.0', '4.1', '4.2',
         '5.0', '5.1', '5.2']

framerate = ['5', '10', '12', '15', '23.976', '24', '25',
             '29.97', '30', '50', '59.94', '60']

aspect_ratio = ['1.33', '1.66', '1.78', '1.85', '2.35', '2.40']

deteline = ['Off', 'Default', 'Custom']

decomb = ['Off', 'Default', 'Fast', 'Bob', 'Custom']

deinterlace = ['Off', 'Fast', 'Slow', 'Slower', 'Bob', 'Custom']

denoise = ['Off', 'Weak', 'Medium', 'Strong', 'Custom']
