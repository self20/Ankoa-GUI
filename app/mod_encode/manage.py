#!/usr/bin/kivy


# Manage Encode MODE
def encode(rls_source, rls_title, reso, crop_width, crop_height,
           crop_top, crop_bottom, crop_right, crop_left, deinterlace,
           motion_deint, denoise, decimate, container, video_ID,
           movie_name, codec, crf, dual_pass, framerate, preset,
           tune, profile, level, audio_ID, audio_title, audio_codec,
           audio_bitrate, audio_samplerate, audio_gain, subs_ID,
           subs_title, subs_forced, subs_burned, subs_default,
           subs_chars, subs_delay, threads_nb, threads_mod, ref_frames,
           max_Bframes, mixed_ref, pyramid_mod, transform, cabac,
           direct_mod, B_frames, weighted_bf, weighted_pf, me_method,
           subpixel, me_range, partitions, trellis, adapt_strenght,
           psy_optim, distord_rate, psy_trellis, deblock_alpha,
           deblock_beta, key_interval, min_key, lookahead, scenecut,
           chroma, fast_skip, grayscale, bluray_compat):

    # FFMPEG CRF
    # if dual_pass is None:
    #
    #     'ffmpeg -i {0} -pass 1 -map 0:{1}{2}{3} -f {5}{6} -'
    #     'c:v:0 {7} -b:v:0 {8}k -level {9}{10} -an -sn -passlogfile '
    #     '{11}{12}.log {11}{12}{13}{14} && ffmpeg -y -i {1} -pass 2 '
    #     '-metadata title='{11}{12}' -metadata proudly.presented.by=''
    #     '{15}' -map 0:{2}{16}{4} -metadata:s:v:0 title= -metadata:s:v'
    #     ':0 language= -f {5}{6} -c:v:0 {7} -b:v:0 {8}k -level {9}{17}'
    #     '{18}{19} -passlogfile {11}{12}.log {11}{12}{13}{14}'
    #     .format(rls_source, video_ID, )



    print (
        rls_source, rls_title, reso, crop_width, crop_height,
        crop_top, crop_bottom, crop_right, crop_left, deinterlace,
        motion_deint, denoise, decimate, container, codec, crf,
        dual_pass, framerate, preset, tune, profile, level,
        audio_ID, audio_title, audio_codec, audio_bitrate,
        audio_samplerate, audio_gain, subs_ID, subs_title,
        subs_forced, subs_burned, subs_default, subs_chars,
        subs_delay, threads_nb, threads_mod, ref_frames,
        max_Bframes, mixed_ref, pyramid_mod, transform, cabac,
        direct_mod, B_frames, weighted_bf, weighted_pf, me_method,
        subpixel, me_range, partitions, trellis, adapt_strenght,
        psy_optim, distord_rate, psy_trellis, deblock_alpha,
        deblock_beta, key_interval, min_key, lookahead, scenecut,
        chroma, fast_skip, grayscale, bluray_compat)
