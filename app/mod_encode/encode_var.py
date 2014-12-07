#!/usr/bin/kivy
# Required variables [ENCODE MODE]

fixed_size = ['350MiB', '550MiB', '700MiB', '1.37GiB',
              '2.05GiB', '2.74GiB', '4.37GiB', '6.56GiB']

audio_bitrate = ['96Kbps', '128Kbps', '192Kbps', '256Kbps',
                 '320Kbps', '384Kbps', '448Kbps', '640Kbps',
                 '755Kbps', '1509Kbps']

sample_rate = ['24kHz', '32kHz', '44kHz', '48kHz', '96kHz']

audio_gain = ['-20', '-19', '-18', '-17', '-16', '-15', '-14', '-13',
              '-12', '-11', '-10', '-9', '-8', '-7', '-6', '-5', '-4',
              '-3', '-2', '-1', '0', '1', '2', '3', '4', '5', '6', '7',
              '8', '9', '10', '11', '12', '13', '14', '15', '16', '17',
              '18', '19', '20']

ar_sd = ['720x540', '720x432', '720x404',
         '720x390', '720x306', '720x300']

ar_720p = ['1280x960', '1280x768', '1280x720',
           '1280x690', '1280x544', '1280x536']

ar_1080p = ['1440x1080', '1800x1080', '1920x1080',
            '1920x1040', '1920x816', '1920x800']

preset = ['Off', 'UltraFast', 'SuperFast', 'VeryFast', 'Faster',
          'Fast', 'Slow', 'Slower', 'VerySlow', 'Placebo']

tune = ['Off', 'Film', 'Animation', 'Grain',
        'Still Image', 'PSNR', 'SSIM', 'Fast Decode']

profile = ['Auto', 'Baseline', 'Main', 'High']

level = ['1.0', '1.1', '1.2', '1.3', '2.0', '2.1', '2.2',
         '3.0', '3.1', '3.2', '4.0', '4.1', '4.2',
         '5.0', '5.1', '5.2']

framerate = ['5', '10', '12', '15', '23.976', '24', '25',
             '29.97', '30', '50', '59.94', '60']

aspect_ratio = ['1.33', '1.66', '1.78', '1.85', '2.35', '2.40']

deinterlace = ['Off', 'Fast', 'Slow', 'Slower', 'VerySlow',
               'Yadif Default', 'Yadif All', 'Custom']

deint_cmd = ['',
             'w3fdif=filter=simple:deint=interlaced',
             'w3fdif=filter=simple:deint=all',
             'w3fdif=filter=complex:deint=interlaced',
             'w3fdif=filter=complex:deint=all',
             'yadif=deint=1', 'yadif=deint=0', '']

motion_deint = ['Off', 'Fast', 'Medium', 'Slow', 'ExtraSlow', 'Custom']

motion_cmd = ['', 'mcdeint=fast', 'mcdeint=medium',
              'mcdeint=slow', 'mcdeint=extra_slow', '']

denoise = ['Off', 'Weak', 'Medium', 'Strong', 'Custom']

denoise_cmd = ['', 'dctdnoiz=0', 'dctdnoiz=4.5', 'dctdnoiz=15:n=4', '']

decimate = ['Off', 'Default', 'Custom']

decimate_cmd = ['', 'cycle=5:scthresh=15:ppsrc=0', '']

pyramidal_method = ['Off', 'Normal', 'Strict']

direct_mode = ['Off', 'Spatial', 'Temporal', 'Auto']

adaptive_bframes = ['VeryFast', 'Fast', 'Slower']

weighted_bframes = ['Off', 'Simple', 'Smart']

motion_method = ['DIA', 'HEX', 'UMH', 'ESA', 'TESA']

partitions_type = ['None', 'All', 'p8x8', 'p4x4',
                   'b8x8', 'i8x8', 'i4x4']

trellis_val = ['Off', 'Default', 'All']

quantization = ['0.0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6',
                '0.7', '0.8', '0.9', '0', '1.1', '1.2', '1.3',
                '1.4', '1.5', '1.6', '1.7', '1.8', '1.9', '2.0']

rate_distortion = ['0.0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6',
                   '0.7', '0.8', '0.9', '1.0', '1.1', '1.2', '1.3',
                   '1.4', '1.5', '1.6', '1.7', '1.8', '1.9', '2.0']

psy_trellis = ['0.00', '0.05', '0.10', '0.15', '0.20', '0.25', '0.30',
               '0.35', '0.40', '0.45', '0.50', '0.55', '0.60', '0.65',
               '0.70', '0.75', '0.80', '0.85', '0.90', '0.95', '1.0']

deblocking = ['-6', '-5', '-4', '-3', '-2', '-1',
              '0', '1', '2', '3', '4', '5', '6']
