#!/usr/bin/kivy
'''
[ MODE ENCODE ]
Manage all content to return proper FFMPEG cmd
'''


# Encode Management
def encode_manager(o_o):

    # Set empty values (will be included in cmd)
    [video_filter, crop, threads_nb, threads_mod, ref_frames,
     fast1pass, max_bf, mixed_ref, pyramid_mod, transform,
     cabac, direct_mod, B_frames, weighted_pf, weighted_bf,
     me_method, subpixel, me_range, partitions, trellis,
     adapt_strenght, psy_optim, psy_rd, deblock_alpha,
     key_interval, min_key, lookahead, scenecut, chroma,
     fast_skip, grayscale, bluray_on] = ['', ] * 32

    # ---------------------------------------------------------------
    #  VIDEO TRACK ##################################################
    # ---------------------------------------------------------------

    # Video Filters
    if o_o['deinterlace'] or o_o['motion_deint'] or\
            o_o['denoise'] or o_o['decimate'] or\
            o_o['crop_width']:

        if o_o['crop_width']:
            crop = ' crop={0}:{1}:{2}:{3}'.format(
                o_o['crop_width'], o_o['crop_height'],
                o_o['crop_right_left'], o_o['crop_top_bottom'])

        video_filter = ' -filter:v{0}{1}{2}{3}{4}'.format(
            crop, o_o['deinterlace'], o_o['motion_deint'],
            o_o['denoise'], o_o['decimate'])

    # Video Resolution
    if len(o_o['resolution']) == 2:
        video_reso = '-s {0}x{1}'.format(
            o_o['resolution'][0], o_o['resolution'][1])
    else:
        video_reso = '-sar {}'.format(o_o['resolution'][0])

    # ---------------------------------------------------------------
    #  ADVANCED #####################################################
    # ---------------------------------------------------------------
    '''Advanced video parameters'''

    if o_o['threads_nb']:
        threads_nb = ' -threads {}'.format(o_o['threads_nb'])
    if o_o['threads_mod']:
        threads_mod = ' -thread_type {}'.format(o_o['threads_mod'])
    if o_o['fast1pass']:
        fast1pass = ' -fastfirstpass {}'.format(o_o['fast1pass'])
    if o_o['ref_frames']:
        ref_frames = ' -refs {}'.format(o_o['ref_frames'])
    if o_o['max_Bframes']:
        max_bf = ' -bf {}'.format(o_o['max_Bframes'])
    if o_o['mixed_ref']:
        mixed_ref = ' -mixed-refs {}'.format(o_o['mixed_ref'])
    if o_o['pyramid_mod']:
        pyramid_mod = ' -b-pyramid {}'.format(o_o['pyramid_mod'].lower())
    if o_o['transform']:
        transform = ' -8x8dct {}'.format(o_o['transform'])
    if o_o['cabac']:
        cabac = ' -coder {}'.format(o_o['cabac'])
    if o_o['direct_mod']:
        direct_mod = ' -direct-pred {}'.format(o_o['direct_mod'].lower())
    if o_o['B_frames']:
        B_frames = ' -b_strategy {}'.format(o_o['B_frames'].lower())
    if o_o['weighted_pf']:
        weighted_pf = ' -weightp {}'.format(o_o['weighted_pf'].lower())
    if o_o['weighted_bf']:
        weighted_bf = ' -weightb {}'.format(o_o['weighted_bf'])
    if o_o['me_method']:
        me_method = ' -me_method {}'.format(o_o['me_method'].lower())
    if o_o['subpixel']:
        subpixel = ' -subq {}'.format(o_o['subpixel'])
    if o_o['me_range']:
        me_range = ' -me_range {}'.format(o_o['me_range'])
    if o_o['partitions']:
        partitions = ' -partitions {}'.format(o_o['partitions'].lower())
    if o_o['trellis']:
        trellis = ' -trellis {}'.format(o_o['trellis'])
    if o_o['adapt_strenght']:
        adapt_strenght = ' -aq-strength {}'.format(o_o['adapt_strenght'])
    if o_o['psy_optim']:
        psy_optim = ' -psy {}'.format(o_o['psy_optim'])
    if o_o['distord_rate']:
        psy_rd = ' -psy-rd {0}:{1}'.format(o_o['distord_rate'],
                                           o_o['psy_trellis'])
    if o_o['deblock_alpha']:
        deblock = ' -deblock {0}:{1}'.format(o_o['deblock_alpha'],
                                             o_o['deblock_beta'])
    if o_o['key_interv']:
        key_interval = ' -g {}'.format(o_o['key_interv'])
    if o_o['min_key']:
        min_key = ' -keyint_min {}'.format(o_o['min_key'])
    if o_o['lookahead']:
        lookahead = ' -rc-lookahead {}'.format(o_o['lookahead'])
    if o_o['scenecut']:
        scenecut = ' -sc_threshold {}'.format(o_o['scenecut'])
    if o_o['chroma']:
        chroma = ' -cmp {}'.format(o_o['chroma'])
    if o_o['fast_skip']:
        fast_skip = ' -fast-pskip {}'.format(o_o['fast_skip'])
    if o_o['grayscale']:
        grayscale = ' -pix_fmt {}'.format(o_o['grayscale'])
    if o_o['bluray']:
        bluray_on = ' -bluray-compat {}'.format(o_o['bluray'])

    # Return video_params cmd
    video_params =  \
        '{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}{11}{12}{13}{14}{15}'\
        '{16}{17}{18}{19}{20}{21}{22}{23}{24}{25}{26}{27}{28}{29}'\
        .format(
            threads_nb, threads_mod, ref_frames, fast1pass, max_bf,
            mixed_ref, pyramid_mod, transform, cabac, direct_mod,
            B_frames, weighted_pf, weighted_bf, me_method, subpixel,
            me_range, partitions, trellis, adapt_strenght, psy_optim,
            psy_rd, deblock_alpha, key_interval, min_key, lookahead,
            scenecut, chroma, fast_skip, grayscale, bluray_on)

    # ---------------------------------------------------------------
    #  AUDIO TRACKS #################################################
    # ---------------------------------------------------------------
    audio_config = []
    for nb in range(0, len(o_o['audio_ID'])):

        # DTS Tracks
        if o_o['audio_bitrate'][nb] == 'dts_copy':
            audio_config.append(
                " -map 0:{0} -c:a:{4} copy -af:a:{4} 'volume={1}db'"
                " -metadata:s:a:{4} title='{2}' -metadata:s:a:{4} "
                "language='{3}'".format(
                    o_o['audio_ID'][nb], o_o['audio_gain'][nb],
                    o_o['audio_title'][nb], o_o['audio_lang'][nb], nb))

        # MP3/AAC/AC3 Tracks
        else:
            audio_config.append(
                " -map 0:{0} -c:a:{8} {1} -b:a:{8} {2}k -ac:a:{8} "
                "{3} -ar:a:{8} {4} -af:a:{8} 'volume={5}dB' -metad"
                "ata:s:a:{8} title='{6}' -metadata:s:a:{8} languag"
                "e='{6}'".format(
                    o_o['audio_ID'][nb], o_o['audio_codec'][nb],
                    o_o['audio_bitrate'][nb], o_o['audio_channels'][nb],
                    o_o['audio_samplerate'][nb], o_o['audio_gain'][nb],
                    o_o['audio_title'][nb], o_o['audio_lang'][nb], nb))
        nb = nb + 1

    # ---------------------------------------------------------------
    #  SUBTITLES TRACKS #############################################
    # ---------------------------------------------------------------
    subtitles_config = []
    for nb in range(0, len(o_o['subs_type'])):

        # Subs File Tracks muxed
        if o_o['subs_type'][nb] == 'subfile' and\
                not o_o['subs_burned'][nb]:
            subtitles_config.append(
                " -map 0:{0} -c:s:{5} {1} -sub_charenc {2} -forced_"
                "subs_only {3} -metadata:s:s:{5} language={4}"
                .format(
                    o_o['subs_source'][nb], o_o['subs_codec'][nb],
                    o_o['subs_charset'][nb], o_o['subs_forced'][nb],
                    o_o['subs_lang'][nb], nb))

        # Subs Source Tracks muxed
        elif o_o['subs_type'][nb] == 'subtrack' and\
                not o_o['subs_burned'][nb]:
            subtitles_config.append(
                " -c:s:{4} {0} -sub_charenc {1} -forced_"
                "subs_only {2} -metadata:s:s:{4} language={3}"
                .format(
                    o_o['subs_source'][nb], o_o['subs_codec'][nb],
                    o_o['subs_charset'][nb], o_o['subs_forced'][nb],
                    o_o['subs_lang'][nb], nb))

        # Subs File Tracks burned
        elif o_o['subs_type'][nb] == 'subfile' and\
                o_o['subs_burned'][nb]:
            subtitles_config.append(
                " subtitles={}".format(o_o['subs_source'][nb]))

        # Subs Source Tracks burned
        elif o_o['subs_type'][nb] == 'subtrack' and\
                o_o['subs_burned'][nb]:
            subtitles_config.append(
                " subtitles={}:si={}".format(
                    o_o['rls_source'][nb], o_o['subs_source'][nb]))
        nb = nb + 1

    print (o_o)

    # ---------------------------------------------------------------
    #  FFMPEG CMD ###################################################
    # ---------------------------------------------------------------
    # FFMPEG CRF
    # if crf is not None:
    #     ffmpeg = \
    #         "ffmpeg -i {0} -map_metadata -1 -metadata title='{1}' "\
    #         "-metadata proudly.presented.by='{2}' -map 0:{3} -r {4}"\
    #         " -f {5} {6} -c:v:0 {7} -crf {8} -level {9}{10}{11}{12}"\
    #         " -passlogfile {1}.log {13}"\
    #         .format(
    #             rls_source, movie_name, team_name, framerate, video_filter,
    #             container, video_reso, codec, crf, level, video_params,
    #             subtitles_config, audio_config, output)
    #
    # FFMPEG 2PASS
    # else:
    #     ffmpeg = \
    #         "ffmpeg -i {0} -pass 1 -map 0:{3} -r {4} -f {5} {6} "\
    #         "c:v:0 {7} -b:v:0 {8}k -level {9}{10} -an -sn -passlogfile "\
    #         "{1}.log {13} && ffmpeg -y -i {0} -pass 2 -map_metadata -1 "\
    #         "-metadata title='{1}' -metadata proudly.presented.by='{2}'"\
    #         " -map 0:{3} -r {4} -f {5} {6} -c:v:0 {7} -b:v:0 {8}k -level"\
    #         " {9}{10}{11}{12} -passlogfile {1}.log {13}"
    #         .format(
    #             rls_source, movie_name, team_name, framerate, video_filter,
    #             container, video_reso, codec, dual_pass, level, video_params,
    #             subtitles_config, audio_config, output)
    #
    # return ffmpeg

    ''' MISSING => subtitles_config, output and users settings '''
