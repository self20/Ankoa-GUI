#!/usr/bin/kivy
'''
[ MODE ENCODE ]
Manage all content to return FFMPEG cmd
'''
from app.mod_encode.encode_dict import o_o
from app.settings.conf_dict import user


# ---------------------------------------------------------------
#  VIDEO TRACK ##################################################
# ---------------------------------------------------------------
def manage_video():

    # Output
    o_o['rls_output'] = '{0}{1}.{2}'.format(
        user['dest_folder'], o_o['rls_title'],
        str(o_o['container'].replace('matroska', 'mkv')))

    # Filters
    if o_o['deinterlace'] or o_o['motion_deint'] or\
            o_o['denoise'] or o_o['decimate'] or\
            o_o['crop_width']:

        if o_o['crop_width']:
            o_o['crop'] = ' crop={0}:{1}:{2}:{3}'.format(
                o_o['crop_width'], o_o['crop_height'],
                o_o['crop_right_left'], o_o['crop_top_bottom'])

        o_o['video_filter'] = ' -vf{0}{1}{2}{3}{4}'.format(
            o_o['crop'], o_o['deinterlace'], o_o['motion_deint'],
            o_o['denoise'], o_o['decimate'])

    # Resolution
    if o_o['resolution']:
        o_o['resolution'] = '-s {}'.format(o_o['resolution'])

    elif o_o['sar']:
        o_o['resolution'] = '-sar {}'.format(o_o['sar'])

    # Preset
    if o_o['preset']:
        o_o['preset'] = ' -preset {}'.format(o_o['preset'].lower())

    # Tune
    if o_o['tune']:
        o_o['tune'] = ' -tune {}'.format(o_o['tune'].lower())

    # Profile
    if o_o['profile']:
        o_o['profile'] = ' -profile:v {}'.format(o_o['profile'].lower())


# ---------------------------------------------------------------
#  AUDIO TRACKS #################################################
# ---------------------------------------------------------------
def manage_audio():
    audio_tracks_list = []
    for nb in range(0, len(o_o['audio_ID'])):

        # DTS
        if o_o['audio_bitrate'][nb] == 'dts_copy':
            audio_tracks_list.append(
                " -map 0:{0} -c:a:{4} copy -af:a:{4} 'volume={1}db'"
                " -metadata:s:a:{4} title='{2}' -metadata:s:a:{4} "
                "language='{3}'".format(
                    o_o['audio_ID'][nb], o_o['audio_gain'][nb],
                    o_o['audio_title'][nb], o_o['audio_lang'][nb], nb))

        # MP3/AAC/AC3
        else:
            audio_tracks_list.append(
                " -map 0:{0} -c:a:{8} {1} -b:a:{8} {2}k -ac:a:{8} "
                "{3} -ar:a:{8} {4} -af:a:{8} 'volume={5}dB' -metad"
                "ata:s:a:{8} title='{6}' -metadata:s:a:{8} languag"
                "e='{7}'".format(
                    o_o['audio_ID'][nb], o_o['audio_codec'][nb],
                    o_o['audio_bitrate'][nb], o_o['audio_channels'][nb],
                    o_o['audio_samplerate'][nb], o_o['audio_gain'][nb],
                    o_o['audio_title'][nb], o_o['audio_lang'][nb], nb))

    o_o['audio_config'] = ''.join(audio_tracks_list)


# ---------------------------------------------------------------
#  SUBTITLES TRACKS #############################################
# ---------------------------------------------------------------
def manage_subs():
    subtitles_tracks_list = []
    for nb in range(0, len(o_o['subs_type'])):

        # Muxed
        if not o_o['subs_burned'][nb]:

            if o_o['subs_type'][nb] == 'subtrack':
                subtitles_tracks_list.append(
                    " -map 0:{0} -c:s:{5} {1} -sub_charenc {2} -forced_"
                    "subs_only {3} -metadata:s:s:{5} language={4}"
                    .format(
                        o_o['subs_source'][nb], o_o['subs_codec'][nb],
                        o_o['subs_charset'][nb], o_o['subs_forced'][nb],
                        o_o['subs_lang'][nb], nb))

            elif o_o['subs_type'][nb] == 'subfile':
                subtitles_tracks_list.append(
                    " -c:s:{5} {1} -sub_charenc {2} -forced_"
                    "subs_only {3} -metadata:s:s:{5} language={4} {0}"
                    .format(
                        o_o['subs_source'][nb], o_o['subs_codec'][nb],
                        o_o['subs_charset'][nb], o_o['subs_forced'][nb],
                        o_o['subs_lang'][nb], nb))

        # Burned
        elif o_o['subs_burned'][nb]:

            # Text based
            if o_o['subs_codec'][nb] == 'ass' or\
                    o_o['subs_codec'][nb] == 'srt':

                if o_o['subs_type'][nb] == 'subfile':
                    subtitles_tracks_list.append(
                        " subtitles={}".format(o_o['subs_source'][nb]))

                elif o_o['subs_type'][nb] == 'subtrack':
                    subtitles_tracks_list.append(
                        " subtitles={0}:si={1}".format(
                            o_o['rls_source'][nb], o_o['subs_source'][nb]))

            # Picture based
            else:
                if o_o['subs_type'][nb] == 'subfile':
                    subtitles_tracks_list.append(
                        " -filter_complex 'overlay[{0}]' -map '[{0}]'"
                        .format(o_o['subs_source'][nb]))

                elif o_o['subs_type'][nb] == 'subtrack':
                    subtitles_tracks_list.append(
                        " -filter_complex 'overlay[0:s:{0}]'"
                        " -map '[0:s:{0}]'".format(
                            o_o['subs_source'][nb]))

    o_o['subs_config'] = ''.join(subtitles_tracks_list)


# ---------------------------------------------------------------
#  ADVANCED PARAM ###############################################
# ---------------------------------------------------------------
def manage_advanced():

    # Append cmd when used
    if o_o['threads_nb']:
        o_o['threads_nb'] = ' -threads {}'.format(o_o['threads_nb'])
    if o_o['threads_mod']:
        o_o['threads_mod'] = ' -thread_type {}'.format(o_o['threads_mod'])
    if o_o['fast1pass']:
        o_o['fast1pass'] = ' -fastfirstpass {}'.format(o_o['fast1pass'])
    if o_o['ref_frames']:
        o_o['ref_frames'] = ' -refs {}'.format(o_o['ref_frames'])
    if o_o['max_Bframes']:
        o_o['max_Bframes'] = ' -bf {}'.format(o_o['max_Bframes'])
    if o_o['mixed_ref']:
        o_o['mixed_ref'] = ' -mixed-refs {}'.format(o_o['mixed_ref'])
    if o_o['pyramid_mod']:
        o_o['pyramid_mod'] = ' -b-pyramid {}'.format(
            o_o['pyramid_mod'].lower())
    if o_o['transform']:
        o_o['transform'] = ' -8x8dct {}'.format(o_o['transform'])
    if o_o['cabac']:
        o_o['cabac'] = ' -coder {}'.format(o_o['cabac'])
    if o_o['direct_mod']:
        o_o['direct_mod'] = ' -direct-pred {}'.format(
            o_o['direct_mod'].lower())
    if o_o['B_frames']:
        o_o['B_frames'] = ' -b_strategy {}'.format(
            o_o['B_frames'].lower())
    if o_o['weighted_pf']:
        o_o['weighted_pf'] = ' -weightp {}'.format(
            o_o['weighted_pf'].lower())
    if o_o['weighted_bf']:
        o_o['weighted_bf'] = ' -weightb {}'.format(o_o['weighted_bf'])
    if o_o['me_method']:
        o_o['me_method'] = ' -me_method {}'.format(
            o_o['me_method'].lower())
    if o_o['subpixel']:
        o_o['subpixel'] = ' -subq {}'.format(o_o['subpixel'])
    if o_o['me_range']:
        o_o['me_range'] = ' -me_range {}'.format(o_o['me_range'])
    if o_o['partitions']:
        o_o['partitions'] = ' -partitions {}'.format(
            o_o['partitions'].lower())
    if o_o['trellis']:
        o_o['trellis'] = ' -trellis {}'.format(o_o['trellis'])
    if o_o['adapt_strenght']:
        o_o['adapt_strenght'] = ' -aq-strength {}'.format(
            o_o['adapt_strenght'])
    if o_o['psy_optim']:
        o_o['psy_optim'] = ' -psy {}'.format(o_o['psy_optim'])
    if o_o['distord_rate']:
        o_o['distord_rate'] = ' -psy-rd {0}:{1}'.format(
            o_o['distord_rate'], o_o['psy_trellis'])
    if o_o['deblock_alpha']:
        o_o['deblock_alpha'] = ' -deblock {0}:{1}'.format(
            o_o['deblock_alpha'], o_o['deblock_beta'])
    if o_o['key_interv']:
        o_o['key_interv'] = ' -g {}'.format(o_o['key_interv'])
    if o_o['min_key']:
        o_o['min_key'] = ' -keyint_min {}'.format(o_o['min_key'])
    if o_o['lookahead']:
        o_o['lookahead'] = ' -rc-lookahead {}'.format(o_o['lookahead'])
    if o_o['scenecut']:
        o_o['scenecut'] = ' -sc_threshold {}'.format(o_o['scenecut'])
    if o_o['chroma']:
        o_o['chroma'] = ' -cmp {}'.format(o_o['chroma'])
    if o_o['fast_skip']:
        o_o['fast_skip'] = ' -fast-pskip {}'.format(o_o['fast_skip'])
    if o_o['grayscale']:
        o_o['grayscale'] = ' -pix_fmt {}'.format(o_o['grayscale'])
    if o_o['bluray']:
        o_o['bluray'] = ' -bluray-compat {}'.format(o_o['bluray'])


def build_advanced():
    o_o['advanced'] =  \
        ' {0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}{11}{12}{13}{14}{15}'\
        '{16}{17}{18}{19}{20}{21}{22}{23}{24}{25}{26}{27}{28}{29}'\
        .format(
            o_o['threads_nb'], o_o['threads_mod'], o_o['ref_frames'],
            o_o['fast1pass'], o_o['max_Bframes'], o_o['mixed_ref'],
            o_o['pyramid_mod'], o_o['transform'], o_o['cabac'],
            o_o['direct_mod'], o_o['B_frames'], o_o['weighted_pf'],
            o_o['weighted_bf'], o_o['me_method'], o_o['subpixel'],
            o_o['me_range'], o_o['partitions'], o_o['trellis'],
            o_o['adapt_strenght'], o_o['psy_optim'], o_o['distord_rate'],
            o_o['deblock_alpha'], o_o['key_interv'], o_o['min_key'],
            o_o['lookahead'], o_o['scenecut'], o_o['chroma'],
            o_o['fast_skip'], o_o['grayscale'], o_o['bluray'])


# ---------------------------------------------------------------
#  FFMPEG CMD ###################################################
# ---------------------------------------------------------------
def manage_ffmpeg():

    # CRF
    if o_o['crf_mode']:
        o_o['ffmpeg'] = \
            "ffmpeg -i {0} -map_metadata -1 -metadata title='{1}' "\
            "-metadata proudly.presented.by='{2}' -map 0:{3} -r {4}"\
            " -f {5} -c:v:0 {6} {7}{8} -crf {9}{10}{11}{12} -level "\
            "{13}{14}{15}{16} -passlogfile {1}.log {17}{18}"\
            .format(
                o_o['rls_source'], o_o['movie_name'], user['team_name'],
                o_o['video_ID'], o_o['framerate'], o_o['container'],
                o_o['video_codec'], o_o['resolution'], o_o['video_filter'],
                o_o['crf_mode'], o_o['preset'], o_o['tune'], o_o['profile'],
                o_o['level'], o_o['advanced'], o_o['subs_config'],
                o_o['audio_config'], user['dest_folder'], o_o['rls_output'])

    # 2PASS
    elif o_o['dual_pass']:
        o_o['ffmpeg'] = \
            "ffmpeg -i {0} -pass 1 -map 0:{3} -r {4} -f {5} c:v:0 {6}"\
            " {7}{8} -b:v:0 {9}k{10}{11}{12} -level {13}{14} -an -sn "\
            "-passlogfile {1}.log {17}{18} && ffmpeg -y -i {0} -pass "\
            "2 -map_metadata -1 -metadata title='{1}' -metadata proud"\
            "ly.presented.by='{2}' -map 0:{3} -r {4} -f {5} -c:v:0 {6}"\
            " {7}{8} -b:v:0 {9}k{10}{11}{12} -level {13}{14}{15}{16} -"\
            "passlogfile {1}.log {17}{18}"\
            .format(
                o_o['rls_source'], o_o['movie_name'], user['team_name'],
                o_o['video_ID'], o_o['framerate'], o_o['container'],
                o_o['video_codec'], o_o['resolution'], o_o['video_filter'],
                o_o['dual_pass'], o_o['preset'], o_o['tune'], o_o['profile'],
                o_o['level'],  o_o['advanced'], o_o['subs_config'],
                o_o['audio_config'], user['dest_folder'], o_o['rls_output'])
