#!/usr/bin/kivy
'''
[ MODE ENCODE ]
Manage all required values to return proper FFMPEG cmd
'''


# Encode Management
def encode(rls_source, rls_title, reso, crop_width, crop_height,
           crop_top, crop_bottom, crop_right, crop_left, deinterlace,
           motion_deint, denoise, decimate, container, video_ID,
           movie_name, codec, crf, dual_pass, fast1pass, framerate, preset,
           tune, profile, level, audio_ID, audio_title, audio_codec,
           audio_bitrate, audio_samplerate, audio_gain, subs_ID,
           subs_title, subs_forced, subs_burned, subs_default,
           subs_chars, subs_delay, threads_nb, threads_mod, ref_frames,
           max_Bframes, mixed_ref, pyramid_mod, transform, cabac,
           direct_mod, B_frames, weighted_pf, weighted_bf, me_method,
           subpixel, me_range, partitions, trellis, adapt_strenght,
           psy_optim, distord_rate, psy_trellis, deblock_alpha,
           deblock_beta, key_interval, min_key, lookahead, scenecut,
           chroma, fast_skip, grayscale, bluray_compat):

    # Videos Filters
    if deinterlace == '' and motion_deint == '' and\
            denoise == '' and decimate == '' and crop_top is None:
        video_filter = ''
    else:
        crop = ''
        video_filter = ' -filter:v{0}{1}{2}{3}{4}'\
            .format(crop, deinterlace, motion_deint, denoise, decimate)

    # Video Resolution
    if len(reso) == 2:
        video_reso = '-s {0}x{1}'.format(reso[0], reso[1])
    else:
        video_reso = '-sar {}'.format(reso[0])

    # Advanced video params
    if threads_nb != '':
        threads_nb = ' -threads {}'.format(threads_nb)
    if threads_mod != '':
        threads_mod = ' -thread_type {}'.format(threads_mod)
    if fast1pass != '':
        fast1pass = ' -fastfirstpass {}'.format(fast1pass)
    if ref_frames != '':
        ref_frames = ' -refs {}'.format(ref_frames)
    if max_Bframes != '':
        max_Bframes = ' -bf {}'.format(max_Bframes)
    if mixed_ref != '':
        mixed_ref = ' -mixed-refs {}'.format(mixed_ref)
    if pyramid_mod != '':
        pyramid_mod = ' -b-pyramid {}'.format(pyramid_mod.lower())
    if transform != '':
        transform = ' -8x8dct {}'.format(transform)
    if cabac != '':
        cabac = ' -coder {}'.format(cabac)
    if direct_mod != '':
        direct_mod = ' -direct-pred {}'.format(direct_mod.lower())
    if B_frames != '':
        B_frames = ' -b_strategy {}'.format(B_frames.lower())
    if weighted_pf != '':
        weighted_pf = ' -weightp {}'.format(weighted_pf.lower())
    if weighted_bf != '':
        weighted_bf = ' -weightb {}'.format(weighted_bf)
    if me_method != '':
        me_method = ' -me_method {}'.format(me_method.lower())
    if subpixel != '':
        subpixel = ' -subq {}'.format(subpixel)
    if me_range != '':
        me_range = ' -me_range {}'.format(me_range)
    if partitions != '':
        partitions = ' -partitions {}'.format(partitions.lower())
    if trellis != '':
        trellis = ' -trellis {}'.format(trellis)
    if adapt_strenght != '':
        adapt_strenght = ' -aq-strength {}'.format(adapt_strenght)
    if psy_optim != '':
        psy_optim = ' -psy {}'.format(psy_optim)
    if distord_rate != '':
        psy_rd = ' -psy-rd {0}:{1}'.format(distord_rate, psy_trellis)
    if deblock_alpha != '':
        deblock = ' -deblock {0}:{1}'.format(deblock_alpha, deblock_beta)
    if key_interval != '':
        key_interval = ' -g {}'.format(key_interval)
    if min_key != '':
        min_key = ' -keyint_min {}'.format(min_key)
    if lookahead != '':
        lookahead = ' -rc-lookahead {}'.format(lookahead)
    if scenecut != '':
        scenecut = ' -sc_threshold {}'.format(scenecut)
    if chroma != '':
        chroma = ' -cmp {}'.format(chroma)
    if fast_skip != '':
        fast_skip = ' -fast-pskip {}'.format(fast_skip)
    if grayscale != '':
        grayscale = ' -pix_fmt {}'.format(grayscale)
    if bluray_compat != '':
        bluray_compat = ' -bluray-compat {}'.format(bluray_compat)

    # Return video params cmd
    video_params =  \
        '{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}{11}{12}{13}{14}{15}'\
        '{16}{17}{18}{19}{20}{21}{22}{23}{24}{25}{26}{27}{28}{29}'\
        .format(
            threads_nb, threads_mod, ref_frames, fast1pass, max_Bframes,
            mixed_ref, pyramid_mod, transform, cabac, direct_mod,
            B_frames, weighted_pf, weighted_bf, me_method, subpixel,
            me_range, partitions, trellis, adapt_strenght, psy_optim,
            psy_rd, deblock, key_interval, min_key, lookahead, scenecut,
            chroma, fast_skip, grayscale, bluray_compat)

    # Audio config
    if len(audio_ID) > 0:
        for audio_track in audio_ID:
            audio_config = ' -c:a:0 {} -b:a:0 {}k -ac:a:0 {}'

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
    #             audio_config, subtitles_config, output)
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
    #             audio_config, subtitles_config, output)
    #
    # return ffmpeg

    # MISSING => audio_config, subtitles_config, output and users settings

    print (
        rls_source, rls_title, reso, crop_width, crop_height,
        crop_top, crop_bottom, crop_right, crop_left, deinterlace,
        motion_deint, denoise, decimate, container, video_ID,
        movie_name, codec, crf, dual_pass, framerate, preset,
        tune, profile, level, audio_ID, audio_title, audio_codec,
        audio_bitrate, audio_samplerate, audio_gain, subs_ID,
        subs_title, subs_forced, subs_burned, subs_default,
        subs_chars, subs_delay, threads_nb, threads_mod, ref_frames,
        max_Bframes, mixed_ref, pyramid_mod, transform, cabac,
        direct_mod, B_frames, weighted_pf, weighted_bf, me_method,
        subpixel, me_range, partitions, trellis, adapt_strenght,
        psy_optim, distord_rate, psy_trellis, deblock_alpha,
        deblock_beta, key_interval, min_key, lookahead, scenecut,
        chroma, fast_skip, grayscale, bluray_compat)
