#!/usr/bin/kivy
__version__ = 'Ankoa v0.1'

import os
import sys
import kivy
kivy.require('1.8.0')
from kivy.app import App
from kivy.compat import PY2
from kivy.lang import Builder
from kivy.config import Config
from os.path import (dirname, join)
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen
from kivy.core.clipboard import Clipboard
from kivy.properties import (NumericProperty, StringProperty,
                             ObjectProperty, ListProperty)
# Local libraries
from app.mod_encode.manager import (manage_video, manage_audio,
                                    manage_subs, manage_advanced,
                                    build_advanced, manage_ffmpeg)
from app.settings.config import (load_settings, modify_settings,
                                 clear_settings)
from app.mod_encode.encode_dict import (o_o, error)
from app.mod_encode.bitrate_cal import calculator
from app.settings.conf_dict import user
from app.scan.scan_source import scan
from app.popup.popup_classes import *
from app.server.remote import remote

# Resolution
Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '768')


# Container
class AnkoaScreen(Screen):
    pass


# Ankoa-GUI
class AnkoaApp(App):

    # ---------------------------------------------------------------
    #  BIND EVENTS ##################################################
    # ---------------------------------------------------------------

    index = NumericProperty(-1)
    screen_names = ListProperty([])
    current_title = StringProperty()
    current_bitrate = StringProperty()
    scan_encode = ObjectProperty()
    scan_remux = ObjectProperty()
    encode_source = StringProperty()
    remux_source = StringProperty()
    audio_count = NumericProperty(0)
    sub_count = NumericProperty(0)
    current_track = ObjectProperty()
    current_error = StringProperty()

    # ---------------------------------------------------------------
    #  ROOT #########################################################
    # ---------------------------------------------------------------
    def build(self):
        self.title = __version__

        # Set screens
        self.screens = {}
        self.menu_screens = sorted([
            'Encode', 'Remux', 'Extract', 'NFOgen',
            'Genprez', 'Thumbnails', 'Torrent'])
        self.screen_names = self.menu_screens

        # Join screens to corresponding kv files
        self.menu_screens = [
            join(dirname(__file__), 'data', 'screen',
                 'mod_{}.kv'.format(fn)) for fn in self.menu_screens]

        # Display 1st screen on open
        self.go_next_screen()

        # Get ENCODE_MODE screens (layouts)
        self.source_screen = \
            self.root.ids.header_screens.current_screen.ids.source
        self.picture_screen = \
            self.root.ids.header_screens.current_screen.ids.picture
        self.video_screen = \
            self.root.ids.header_screens.current_screen.ids.videox
        self.audio_screen = \
            self.root.ids.header_screens.current_screen.ids.audiox
        self.subtitles_screen = \
            self.root.ids.header_screens.current_screen.ids.subtitles
        self.advanced_screen = \
            self.root.ids.header_screens.current_screen.ids.advanced
        self.queue_screen = \
            self.root.ids.header_screens.current_screen.ids.queue

    # ---------------------------------------------------------------
    #  GLOBAL #######################################################
    # ---------------------------------------------------------------

    # Restart App
    def restart_ankoa(self):
        restart = sys.executable
        os.execl(restart, restart, * sys.argv)

    # Copy to clipboard
    def copy_to_clipboard(self, text):
        Clipboard.put(bytes(text, 'UTF-8'), 'UTF8_STRING')
        Clipboard.get('UTF8_STRING')

    # ---------------------------------------------------------------
    #  USER SETTINGS ################################################
    # ---------------------------------------------------------------
    # Load settings on start / verification
    # Manage save/clear From data.popup.settings To app.settings.config
    # Manage remote session From data.popup.remote To app.server.remote

    # Load user settings on start
    load_settings()

    # Save user settings
    def save_settings(self):
        modify_settings()

    # Clear user settings
    def reset_settings(self):
        clear_settings()

    # Check essential settings
    def check_user_settings(self):
        if user['source_folder'] and user['dest_folder']:
            return True
        else:
            return False

    # Remote session (mount remote folder to local via sshfs)
    def manage_remote(self, request):
        remote(request)

    # ---------------------------------------------------------------
    #  MANAGE POPUPS ################################################
    # ---------------------------------------------------------------

    # Load all popups (kv files)
    for popup in os.listdir('data/popup/'):
        if popup.endswith('.kv'):
            Builder.load_file('data/popup/{}'.format(popup))

    # Display popups
    def main_popup(self, popup_id):
        '''
        Call corresponding class in app.popup.popup_classes
        From anywhere with popup_id request
        '''
        popup = '{}'.format(popup_id)
        eval(popup).open()

    # ---------------------------------------------------------------
    #  MANAGE SCREENS ###############################################
    # ---------------------------------------------------------------

    # Go previous screen
    def go_previous_screen(self):
        self.index = (self.index - 1) % len(self.menu_screens)
        screen = self.load_screen(self.index)
        header_screens = self.root.ids.header_screens
        header_screens.switch_to(screen, direction='right')
        self.current_title = screen.name

    # Go next screen
    def go_next_screen(self):
        self.index = (self.index + 1) % len(self.menu_screens)
        screen = self.load_screen(self.index)
        header_screens = self.root.ids.header_screens
        header_screens.switch_to(screen, direction='left')
        self.current_title = screen.name

    # Go selected screen
    def go_screen(self, current_screen):
        self.index = current_screen
        screen = self.load_screen(self.index)
        self.root.ids.header_screens.switch_to(
            self.load_screen(current_screen), direction='left')
        self.current_title = screen.name

    # Load screen on request
    def load_screen(self, index):
        if index in self.screens:
            return self.screens[index]
        screen = Builder.load_file(self.menu_screens[index].lower())
        self.screens[index] = screen
        return screen

    # ---------------------------------------------------------------
    #  MANAGE LAYOUTS ###############################################
    # ---------------------------------------------------------------

    # Load ENCODE_MODE layouts (kv files)
    for mod_encod_kvs in os.listdir('data/screen/mod_encode/'):
        if mod_encod_kvs.endswith('.kv'):
            Builder.load_file(
                'data/screen/mod_encode/{}'.format(mod_encod_kvs))

    # Load REMUX_MODE layouts (kv files)
    for mod_remux_kvs in os.listdir('data/screen/mod_remux/'):
        if mod_remux_kvs.endswith('.kv'):
            Builder.load_file(
                'data/screen/mod_remux/{}'.format(mod_remux_kvs))

    # ---------------------------------------------------------------
    #  MANAGE SOURCE ################################################
    # ---------------------------------------------------------------

    # Scan video source
    def scan_source_infos(self, source):
        '''
        Return complete mediainfo with autocrop values
        Call app.mod_encode.scan_source.scan
        '''
        if user['request'] == 'encode_source':
            self.scan_encode = scan(source)
        elif user['request'] == 'remux_source':
            self.scan_remux = scan(source)

    # Load Video Source
    def load_video_source(self, source):
        '''
        Get source location on filemanager selection
        Also required by video player preview
        '''
        if user['request'] == 'encode_source':
            self.encode_source = source
        elif user['request'] == 'remux_source':
            self.remux_source = source

    # Get current track
    def get_current_track(self, current_track):
        self.current_track = current_track
        return self.current_track

    # ---------------------------------------------------------------
    #  VIDEO LAYOUT ##################################### ENCODE ####
    # ---------------------------------------------------------------

    # Video bitrate layout
    def toggle_bitrate(self, state):
        '''
        Toggle bitrate row animation (row height on/off)
        From data.screen.mod_encode.video [Bitrate button]
        '''
        if state == 'down':
            height = 42
        else:
            height = 0
        Animation(height=height, d=.1, t='out_quart').start(
            self.video_screen.ids.bitrate_view)

    # Video bitrate calculator
    def bit_calculator(self):
        '''
        Call app.mod_encode.bitrate_calculator
        From data.screen.mod_encode.video [RUN button]
        '''
        current_bitrate = calculator()
        self.current_bitrate = str(current_bitrate)
        return self.current_bitrate

    # ---------------------------------------------------------------
    #  AUDIO LAYOUT ##################################### ENCODE ####
    # ---------------------------------------------------------------
    # Manage audio Tracks (max 5 tracks)
    # From data.screen.mod_encode.audio

    # Load Audio Track (kv file)
    def load_audio_track(self):
        audio_track = Builder.load_file(
            'data/screen/mod_encode/widget/audio_track.kv')
        track_layout = self.audio_screen.ids.audio_track_layout
        return (audio_track, track_layout)

    # Add Audio Track (from source)
    def add_audio_track(self):
        (audio_track, track_layout) = self.load_audio_track()
        if self.audio_count < 5:
            track_layout.add_widget(audio_track)
            self.audio_count += 1

    # Delete current Audio Track
    def del_audio_track(self, current_track):
        (audio_track, track_layout) = self.load_audio_track()
        track_layout.remove_widget(current_track)
        if self.audio_count > 0:
            self.audio_count += -1

    # Clear all Audio Tracks
    def clear_audio_tracks(self):
        (audio_track, track_layout) = self.load_audio_track()
        track_layout.clear_widgets()
        self.audio_count = 0

    # ---------------------------------------------------------------
    #  SUBTITLES LAYOUT ################################# ENCODE ####
    # ---------------------------------------------------------------
    # Manage subtitles Tracks (max 7 tracks)
    # From data.screen.mod_encode.subtitles

    # Load Subtitles Tracks (kv files)
    def load_subtitles_track(self):
        sub_track = Builder.load_file(
            'data/screen/mod_encode/widget/sub_track.kv')
        sub_file = Builder.load_file(
            'data/screen/mod_encode/widget/sub_file.kv')
        track_layout = self.subtitles_screen.ids.sub_track_layout
        return (sub_track, sub_file, track_layout)

    # Add Subtitles Track (from source)
    def add_sub_source_track(self):
        (sub_track, sub_file,
         track_layout) = self.load_subtitles_track()
        if self.sub_count < 7:
            track_layout.add_widget(sub_track)
            self.sub_count += 1

    # Add Subtitles Track (from file)
    def add_sub_file_track(self):
        (sub_track, sub_file,
         track_layout) = self.load_subtitles_track()
        if self.sub_count < 7:
            track_layout.add_widget(sub_file)
            self.sub_count += 1

    # Delete current Subtitles Track
    def del_subtitles_track(self, current_track):
        (sub_track, sub_file,
         track_layout) = self.load_subtitles_track()
        track_layout.remove_widget(current_track)
        if self.sub_count > 0:
            self.sub_count += -1

    # Clear all Subtitles Tracks
    def clear_subtitles_tracks(self):
        (sub_track, sub_file,
         track_layout) = self.load_subtitles_track()
        track_layout.clear_widgets()
        self.sub_count = 0

    # Load Subtitles Source
    def load_sub_source(self, value):
        '''
        Get subfile location from filemanager selection to
        display subfile title in corresponding track area
        '''
        current_track = self.get_current_track(self.current_track)
        current_track.ids.sub_source.text = value.split('/')[-1]
        current_track.ids.sub_codec.value = value.split('.')[-1]

    # ---------------------------------------------------------------
    #  MAPPING ENCODE ###############################################
    # ---------------------------------------------------------------

    # Get encode infos
    def get_encode_infos(self):
        '''
        Get all screens values from corresponding kv file
        Fill in encode dictionary o_o
        '''

        # Get source infos
        o_o['rls_source'] = self.source_screen.ids.source.text
        o_o['rls_title'] = self.source_screen.ids.title.text

        # Get picture infos
        if self.picture_screen.ids.check_sar.active is True:
            o_o['sar'] = self.picture_screen.ids.sar_val.value
        else:
            o_o['resolution'] = '{0}x{1}'.format(
                self.picture_screen.ids.video_W.text,
                self.picture_screen.ids.video_H.text)
        if self.picture_screen.ids.custom_crop.active is True:
            o_o['crop_width'] = self.picture_screen.ids.crop_W.text
            o_o['crop_height'] = self.picture_screen.ids.crop_H.text
            o_o['crop_right_left'] = self.picture_screen.ids.crop_R.text
            o_o['crop_top_bottom'] = self.picture_screen.ids.crop_T.text
        o_o['deinterlace'] = self.picture_screen.ids.deint.text
        o_o['motion_deint'] = self.picture_screen.ids.motion_d.text
        o_o['denoise'] = self.picture_screen.ids.denoise.text
        o_o['decimate'] = self.picture_screen.ids.decimate.text

        # Get video infos
        o_o['video_ID'] = self.video_screen.ids.video_track_ID.text
        o_o['movie_name'] = self.video_screen.ids.movie_name.text
        o_o['container'] = self.video_screen.ids.vcontainer.valueA
        o_o['video_codec'] = self.video_screen.ids.vcontainer.valueB
        if self.video_screen.ids.check_crf.active is True:
            o_o['crf_mode'] = self.video_screen.ids.crf_val.text
        else:
            o_o['dual_pass'] = self.video_screen.ids.video_bitrate.text
            o_o['fast1pass'] = self.video_screen.ids.fast1pass.value
        o_o['framerate'] = self.video_screen.ids.fram_rate.text
        o_o['preset'] = self.video_screen.ids.pre_set.value
        o_o['tune'] = self.video_screen.ids.tu_ne.value
        o_o['profile'] = self.video_screen.ids.pro_file.text
        o_o['level'] = self.video_screen.ids.le_vel.text

        # Get audio infos
        audio = self.audio_screen.ids.audio_track_layout.children
        for nb in range(0, len(audio)):
            o_o['audio_ID'].append(audio[nb].ids.audio_track_ID.text)
            o_o['audio_title'].append(audio[nb].ids.audio_track_title.text)
            o_o['audio_lang'].append(audio[nb].ids.audio_track_lang.text)
            o_o['audio_codec'].append(audio[nb].ids.acodec.value)
            o_o['audio_bitrate'].append(audio[nb].ids.abitrate.value)
            o_o['audio_channels'].append(audio[nb].ids.channels.value)
            o_o['audio_samplerate'].append(audio[nb].ids.sample_rate.text)
            o_o['audio_gain'].append(audio[nb].ids.gain.text)

        # Get subtitles infos
        sub = self.subtitles_screen.ids.sub_track_layout.children
        for nb in range(0, len(sub)):
            o_o['subs_type'].append(sub[nb].ids.sub_infos.type)
            o_o['subs_source'].append(sub[nb].ids.sub_source.text)
            o_o['subs_codec'].append(sub[nb].ids.sub_codec.value)
            o_o['subs_lang'].append(sub[nb].ids.sub_track_lang.text)
            o_o['subs_forced'].append(sub[nb].ids.sub_forced.value)
            o_o['subs_burned'].append(sub[nb].ids.sub_burned.value)
            o_o['subs_charset'].append(sub[nb].ids.sub_charset.text)

        # Get advanced infos
        if self.advanced_screen.ids.threads_on.active is True:
            o_o['threads_nb'] = self.advanced_screen.ids.threads.text
            o_o['threads_mod'] = self.advanced_screen.ids.threads_mod.value
        if self.advanced_screen.ids.frames_on.active is True:
            o_o['ref_frames'] = self.advanced_screen.ids.ref_frames.text
            o_o['max_Bframes'] = self.advanced_screen.ids.max_Bframes.text
            o_o['mixed_ref'] = self.advanced_screen.ids.mixed_ref.value
        if self.advanced_screen.ids.encod_on.active is True:
            o_o['pyramid_mod'] = self.advanced_screen.ids.pyram.value
            o_o['transform'] = self.advanced_screen.ids.transform.value
            o_o['cabac'] = self.advanced_screen.ids.cabac.value
        if self.advanced_screen.ids.adapt_on.active is True:
            o_o['direct_mod'] = self.advanced_screen.ids.direct.value
            o_o['B_frames'] = self.advanced_screen.ids.Bframes.value
        if self.advanced_screen.ids.weight_on.active is True:
            o_o['weighted_pf'] = self.advanced_screen.ids.weight_pf.value
            o_o['weighted_bf'] = self.advanced_screen.ids.weight_bf.value
        if self.advanced_screen.ids.motion_on.active is True:
            o_o['me_method'] = self.advanced_screen.ids.me_mod.text
            o_o['subpixel'] = self.advanced_screen.ids.subpixel.text
            o_o['me_range'] = self.advanced_screen.ids.me_range.text
        if self.advanced_screen.ids.partitions_on.active is True:
            o_o['partitions'] = self.advanced_screen.ids.parts.text
            o_o['trellis'] = self.advanced_screen.ids.trellis.value
        if self.advanced_screen.ids.quantiz_on.active is True:
            o_o['adapt_strenght'] = self.advanced_screen.ids.adapt_s.text
            o_o['psy_optim'] = self.advanced_screen.ids.psy_optim.value
        if self.advanced_screen.ids.distortion_on.active is True:
            o_o['distord_rate'] = self.advanced_screen.ids.dist_rate.text
            o_o['psy_trellis'] = self.advanced_screen.ids.psy_trell.text
        if self.advanced_screen.ids.deblock_on.active is True:
            o_o['deblock_alpha'] = self.advanced_screen.ids.d_alpha.text
            o_o['deblock_beta'] = self.advanced_screen.ids.d_beta.text
        if self.advanced_screen.ids.keyframe_on.active is True:
            o_o['key_interv'] = self.advanced_screen.ids.key_interval.text
            o_o['min_key'] = self.advanced_screen.ids.min_key.text
            o_o['lookahead'] = self.advanced_screen.ids.lookahead.text
        if self.advanced_screen.ids.various_on.active is True:
            o_o['scenecut'] = self.advanced_screen.ids.scenecut.text
            o_o['chroma'] = self.advanced_screen.ids.chroma.value
            o_o['fast_skip'] = self.advanced_screen.ids.fast_skip.value
            o_o['grayscale'] = self.advanced_screen.ids.grayscale.value
            o_o['bluray'] = self.advanced_screen.ids.bluray_compat.value

    # ---------------------------------------------------------------
    #  MANAGE ENCODE ################################################
    # ---------------------------------------------------------------
    # Check content and call the manager app.mod_encode.manager
    # Manager will set proper FFMPEG cmd in dictionary o_o
    # Display popup error on missing values

    # Essential content verification
    def check_encode_values(self):
        if self.check_user_settings() is True and\
                self.source_screen.ids.r_source.active is True and\
                self.source_screen.ids.r_title.active is True and\
                (self.picture_screen.ids.reso.active is True or
                 self.picture_screen.ids.check_sar.active is True) and\
                self.video_screen.ids.check_vtrack.active is True and\
                self.video_screen.ids.check_codec.active is True:
            return True
        else:
            if self.check_user_settings() is False:
                self.current_error = error['settings']
            elif self.source_screen.ids.r_source.active is False:
                self.current_error = error['source']
            elif self.source_screen.ids.r_title.active is False:
                self.current_error = error['title']
            elif self.picture_screen.ids.reso.active is False or\
                    self.picture_screen.ids.check_sar.active is False:
                self.current_error = error['reso']
            elif self.video_screen.ids.check_vtrack.active is False:
                self.current_error = error['video']
            elif self.video_screen.ids.check_codec.active is False:
                self.current_error = error['codec']
            return False

    # Reset dictionary
    def reset_dictionary(self):
        self.queue_screen.ids.ffmpeg_cmd.text = ''
        for key, value in o_o.items():
            if isinstance(value, list):
                o_o[key] = []
            else:
                o_o[key] = ''

    # Get content
    def send_encode_values(self):
        self.get_encode_infos()
        manage_video()
        manage_audio()
        manage_subs()
        manage_advanced()
        build_advanced()
        manage_ffmpeg()
        self.queue_screen.ids.ffmpeg_cmd.text = '{}'.format(o_o['ffmpeg'])

        '''debug'''
        print (str(o_o).replace(", ", "'\n")
                       .replace("],", "]\n"))

if __name__ == '__main__':
    AnkoaApp().run()
