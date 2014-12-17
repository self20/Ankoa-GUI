#!/usr/bin/kivy
'''
[ MODE ENCODE ]
Dictionaries to manage encode:
    o_o > encode parameters
    v_v > parameters options
    u_u > bitrate calculator
    error > missing values messages
'''

o_o = {

    # Source
    'rls_output': '',
    'rls_source': '',
    'rls_title': '',

    # Picture
    'resolution': '',
    'sar': '',
    'crop': '',
    'crop_width': '',
    'crop_height': '',
    'crop_right_left': '',
    'crop_top_bottom': '',
    'video_filter': '',
    'deinterlace': '',
    'motion_deint': '',
    'denoise': '',
    'decimate': '',

    # Video
    'video_ID': '',
    'movie_name': '',
    'container': '',
    'video_codec': '',
    'crf_mode': '',
    'dual_pass': '',
    'fast1pass': '',
    'framerate': '',
    'preset': '',
    'tune': '',
    'profile': '',
    'level': '',

    # Audio
    'audio_ID': [],
    'audio_title': [],
    'audio_lang': [],
    'audio_codec': [],
    'audio_bitrate': [],
    'audio_channels': [],
    'audio_samplerate': [],
    'audio_gain': [],
    'audio_config': '',

    # Subtitles
    'subs_type': [],
    'subs_source': [],
    'subs_codec': [],
    'subs_lang': [],
    'subs_forced': [],
    'subs_burned': [],
    'subs_charset': [],
    'subs_config': '',

    # Advanced
    'max_Bframes': '',
    'ref_frames': '',
    'threads_mod': '',
    'threads_nb': '',
    'mixed_ref': '',
    'B_frames': '',
    'me_range': '',
    'distord_rate': '',
    'key_interv': '',
    'fast_skip': '',
    'grayscale': '',
    'min_key': '',
    'lookahead': '',
    'bluray': '',
    'scenecut': '',
    'chroma': '',
    'deblock_beta': '',
    'deblock_alpha': '',
    'psy_trellis': '',
    'partitions': '',
    'weighted_bf': '',
    'pyramid_mod': '',
    'transform': '',
    'weighted_pf': '',
    'trellis': '',
    'adapt_strenght': '',
    'me_method': '',
    'cabac': '',
    'direct_mod': '',
    'subpixel': '',
    'psy_optim': '',
    'advanced': '',

    # FFMPEG
    'ffmpeg': ''
}

v_v = {

    'fixed_size': ['350MiB', '550MiB', '700MiB', '1.37GiB',
                   '2.05GiB', '2.74GiB', '4.37GiB', '6.56GiB'],

    'mp3_bitrate': ['56Kbps', '64Kbps', '80Kbps', '96Kbps',
                    '112Kbps', '128Kbps', '160Kbps', '192Kbps',
                    '224Kbps', '256Kbps', '320Kbps'],

    'aac_bitrate': ['80Kbps', '96Kbps', '112Kbps', '128Kbps',
                    '160Kbps', '192Kbps', '224Kbps', '256Kbps',
                    '320Kbps', '384Kbps', '448Kbps'],

    'ac3_bitrate': ['96Kbps', '112Kbps', '128Kbps', '160Kbps',
                    '192Kbps', '224Kbps', '256Kbps', '320Kbps',
                    '384Kbps', '448Kbps', '640Kbps'],

    'audio_bitrate': ['56Kbps', '64Kbps', '80Kbps', '96Kbps',
                      '112Kbps', '128Kbps', '160Kbps', '192Kbps',
                      '224Kbps', '256Kbps', '320Kbps', '448Kbps',
                      '640Kbps', '755Kbps', '1509Kbps'],

    'sample_rate': ['24kHz', '32kHz', '44kHz', '48kHz', '96kHz'],

    'audio_gain': ['-20', '-19', '-18', '-17', '-16', '-15', '-14',
                   '-13', '-12', '-11', '-10', '-9', '-8', '-7',
                   '-6', '-5', '-4', '-3', '-2', '-1', '0', '1',
                   '2', '3', '4', '5', '6', '7', '8', '9', '10',
                   '11', '12', '13', '14', '15', '16', '17',
                   '18', '19', '20'],

    'ar_sd': ['720x540', '720x432', '720x404',
              '720x390', '720x306', '720x300'],

    'ar_720p': ['1280x960', '1280x768', '1280x720',
                '1280x690', '1280x544', '1280x536'],

    'ar_1080p': ['1440x1080', '1800x1080', '1920x1080',
                 '1920x1040', '1920x816', '1920x800'],

    'preset': ['Off', 'UltraFast', 'SuperFast', 'VeryFast', 'Faster',
               'Fast', 'Slow', 'Slower', 'VerySlow', 'Placebo'],

    'tune': ['Off', 'Film', 'Animation', 'Grain',
             'Still Image', 'PSNR', 'SSIM', 'Fast Decode'],

    'profile': ['Auto', 'Baseline', 'Main', 'High'],

    'level': ['1.0', '1.1', '1.2', '1.3', '2.0', '2.1',
              '2.2', '3.0', '3.1', '3.2', '4.0', '4.1',
              '4.2', '5.0', '5.1', '5.2'],

    'framerate': ['5', '10', '12', '15', '23.976', '24',
                  '25', '29.97', '30', '50', '59.94', '60'],

    'aspect_ratio': ['1.33', '1.66', '1.78', '1.85', '2.35', '2.40'],

    'deinterlace': ['Off', 'Fast', 'Slow', 'Slower', 'VerySlow',
                    'Yadif Default', 'Yadif All', 'Custom'],

    'deint_cmd': ['',
                  ' w3fdif=filter=simple:deint=interlaced',
                  ' w3fdif=filter=simple:deint=all',
                  ' w3fdif=filter=complex:deint=interlaced',
                  ' w3fdif=filter=complex:deint=all',
                  ' yadif=deint=1', ' yadif=deint=0', ''],

    'motion_deint': ['Off', 'Fast', 'Medium', 'Slow',
                     'ExtraSlow', 'Custom'],

    'motion_cmd': ['', ' mcdeint=fast', ' mcdeint=medium',
                   ' mcdeint=slow', ' mcdeint=extra_slow', ''],

    'denoise': ['Off', 'Weak', 'Medium', 'Strong', 'Custom'],

    'denoise_cmd': ['', ' dctdnoiz=0', ' dctdnoiz=4.5',
                    ' dctdnoiz=15:n=4', ''],

    'decimate': ['Off', 'Default', 'Custom'],

    'decimate_cmd': ['', ' cycle=5:scthresh=15:ppsrc=0', ''],

    'pyramidal_method': ['Off', 'Normal', 'Strict'],

    'direct_mode': ['Off', 'Spatial', 'Temporal', 'Auto'],

    'adaptive_bframes': ['Off', 'VeryFast', 'Fast', 'Slower'],

    'weighted_pframes': ['Off', 'None', 'Simple', 'Smart'],

    'motion_method': ['DIA', 'HEX', 'UMH', 'ESA', 'TESA'],

    'partitions_type': ['None', 'All', 'p8x8', 'p4x4',
                        'b8x8', 'i8x8', 'i4x4'],

    'trellis_val': ['Off', 'Default', 'All'],

    'quantization': ['0.0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6',
                     '0.7', '0.8', '0.9', '0', '1.1', '1.2', '1.3',
                     '1.4', '1.5', '1.6', '1.7', '1.8', '1.9', '2.0'],

    'rate_distortion': ['0.0', '0.1', '0.2', '0.3', '0.4', '0.5',
                        '0.6', '0.7', '0.8', '0.9', '1.0', '1.1',
                        '1.2', '1.3', '1.4', '1.5', '1.6', '1.7',
                        '1.8', '1.9', '2.0'],

    'psy_trellis': ['0.00', '0.05', '0.10', '0.15', '0.20', '0.25',
                    '0.30', '0.35', '0.40', '0.45', '0.50', '0.55',
                    '0.60', '0.65', '0.70', '0.75', '0.80', '0.85',
                    '0.90', '0.95', '1.0'],

    'deblocking': ['-6', '-5', '-4', '-3', '-2', '-1',
                   '0', '1', '2', '3', '4', '5', '6']
}

u_u = {
    'HH': '',
    'MM': '',
    'SS': '',
    'audio_bit': '',
    'desired_size': '',

    'bit_sizes': ['357.8', '562.9', '716.3', '1439.3',
                  '2151', '2875.5', '4585.2', '6881.5'],

    'audiobit': ['56', '64', '80', '96', '112', '128',
                 '160', '192', '224', '256', '320',
                 '448', '640', '755', '1509']
}

error = {
    'settings': 'User settings are not defined !',
    'source': 'No release source selected !',
    'title': 'Please specify release title !',
    'reso': 'Video resolution not specified !',
    'video': 'Specify valid video track ID !',
    'codec': 'Specify video codec output !'
}
