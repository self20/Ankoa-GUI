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
from os.path import dirname, join
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen
from kivy.properties import (NumericProperty, StringProperty,
                             ObjectProperty, ListProperty)

# Local libraries
from app.mod_encode.bitrate_cal import *
from app.mod_encode.scan_source import *
from app.popup.popup_classes import *
from app.popup.settings import *
from app.popup.remote import *

# Resolution
Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '768')


# Container
class AnkoaScreen(Screen):
    pass


# Ankoa-GUI
class AnkoaApp(App):

    # ---------------------------------------------------------------
    #  PROPERTIES ###################################################
    # ---------------------------------------------------------------
    '''kv files interaction'''

    index = NumericProperty(-1)
    screen_names = ListProperty([])
    current_title = StringProperty()
    current_bitrate = StringProperty()
    scan_data = ObjectProperty()
    video_source = StringProperty()
    audio_count = NumericProperty(0)
    sub_count = NumericProperty(0)
    current_track = ObjectProperty()

    # ---------------------------------------------------------------
    #  ROOT #########################################################
    # ---------------------------------------------------------------
    '''Application Root'''

    def build(self):
        self.title = __version__

        # Set screens (MODES)
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

    # ---------------------------------------------------------------
    #  SETTINGS #####################################################
    # ---------------------------------------------------------------

    # Load user settings on start
    '''call app.popup.settings: load_settings()'''
    (source_folder, dest_folder, team_name, tmdb_apikey, tk_announce,
     ssh_host, ssh_port, ssh_username, ssh_passwd,
     remote_folder) = load_settings()

    # Restart app
    def restart_ankoa(self):
        restart = sys.executable
        os.execl(restart, restart, * sys.argv)

    # Save user settings
    def save_settings(self, source_folder, dest_folder, team_name,
                      tmdb_apikey, tk_announce, ssh_host, ssh_port,
                      ssh_username, ssh_passwd, remote_folder, request):
        '''
        Call app.popup.settings.py: save_settings()
        From data.popup: settings.kv [validate settings button]
        '''
        modify_settings(source_folder, dest_folder, team_name,
                        tmdb_apikey, tk_announce, ssh_host, ssh_port,
                        ssh_username, ssh_passwd, remote_folder)

    # Clear user settings
    def reset_settings(self):
        '''
        Call app.popup.settings.py: clear_settings()
        From data.popup: settings.kv [clear settings button]
        '''
        clear_settings()

    # Remote session (mount remote folder to local via sshfs)
    def manage_remote(self, request):
        '''
        Call app.popup.remote.py: remote()
        From data.popup: remote.kv with corresponding request
        request: 'mount_source_track' will mount remote folder
        request: 'umount_source_track' will umount remote folder
        '''
        remote(request, self.ssh_passwd, self.ssh_username,
               self.ssh_host, self.source_folder,
               self.remote_folder, self.ssh_port)

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
        Call app.popup.popup_classes.py: corresponding popup class
        From anywhere with popup_id request (same name as classes)
        '''
        popup = '{}'.format(popup_id)
        eval(popup).open()

    # ---------------------------------------------------------------
    #  MANAGE SCREENS ###############################################
    # ---------------------------------------------------------------

    # Go previous screen (MODES)
    def go_previous_screen(self):
        self.index = (self.index - 1) % len(self.menu_screens)
        screen = self.load_screen(self.index)
        header_screens = self.root.ids.header_screens
        header_screens.switch_to(screen, direction='right')
        self.current_title = screen.name

    # Go next screen (MODES)
    def go_next_screen(self):
        self.index = (self.index + 1) % len(self.menu_screens)
        screen = self.load_screen(self.index)
        header_screens = self.root.ids.header_screens
        header_screens.switch_to(screen, direction='left')
        self.current_title = screen.name

    # Go selected screen (MODES)
    def go_screen(self, current_screen):
        self.index = current_screen
        screen = self.load_screen(self.index)
        self.root.ids.header_screens.switch_to(
            self.load_screen(current_screen), direction='left')
        self.current_title = screen.name

    # Load screen on request (MODES)
    def load_screen(self, index):
        if index in self.screens:
            return self.screens[index]
        screen = Builder.load_file(self.menu_screens[index].lower())
        self.screens[index] = screen
        return screen

    # Load ENCODE_MODE screens (kv files)
    for mod_encod_kvs in os.listdir('data/screen/mod_encode/'):
        if mod_encod_kvs.endswith('.kv'):
            Builder.load_file(
                'data/screen/mod_encode/{}'.format(mod_encod_kvs))

    # ---------------------------------------------------------------
    #  MANAGE TRACKS ################################################
    # ---------------------------------------------------------------

    # Get current track
    def get_current_track(self, current_track):
        self.current_track = current_track
        return self.current_track

    # ---------------------------------------------------------------
    #  VIDEO SCREEN #################################################
    # ---------------------------------------------------------------

    # Scan video source
    def scan_source_infos(self, source):
        '''
        Return complete mediainfo with autocrop values
        Call app.mod_encode.scan_source.py: scan()
        From data.screen.mod_encode.source.kv [scan button]
        '''
        self.scan_data = scan(source)

    # Video bitrate calculator layout
    def toggle_bitrate(self, state):
        '''
        Display bitrate calculator section on clic
        Toggle bitrate row animation (row height on/off)
        From data.screen.mod_encode.video.kv [Bitrate button]
        '''
        if state == 'down':
            height = 50
        else:
            height = 0
        Animation(height=height, d=.3, t='out_quart').start(
            self.video_screen.ids.bitrate_view)

    # Video bitrate calculator function
    def bit_calculator(self, HH, MM, SS, audio_bit, desired_size):
        '''
        Return video bitrate in kbps
        Call app.mod_encode.bitrate_cal.py: calculator()
        From data.screen.mod_encode.video.kv [RUN button]
        '''
        current_bitrate = calculator(HH, MM, SS, audio_bit, desired_size)
        self.current_bitrate = str(current_bitrate)
        return self.current_bitrate

    # Load Video Source
    def load_video_source(self, text):
        '''
        Get source location on filemanager selection
        Required by preview screen (video player)
        '''
        self.video_source = text

    # ---------------------------------------------------------------
    #  AUDIO SCREEN #################################################
    # ---------------------------------------------------------------
    '''
    Manage audio Tracks (max 5 tracks)
    From data.screen.mod_encode.audio.kv
    '''

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
    #  SUBTITLES SCREEN #############################################
    # ---------------------------------------------------------------
    '''
    Manage subtitles Tracks (max 7 tracks)
    From data.screen.mod_encode.subtitles.kv
    '''

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
        current_track.ids.sub_track_title.text = value.split('/')[-1]

    # ---------------------------------------------------------------
    #  MAPPING ENCODE ###############################################
    # ---------------------------------------------------------------
    '''Get all screens values from corresponding kv file'''

    # Get source infos
    def get_source_infos(self):
        '''from data/mod_encode/screen/source.kv'''
        rls_source = self.source_screen.ids.source.text
        rls_title = self.source_screen.ids.title.text
        return (rls_source, rls_title)

    # Get picture infos
    def get_picture_infos(self):
        '''from data/mod_encode/screen/picture.kv'''
        if self.picture_screen.ids.check_sar.active is True:
            reso = [self.picture_screen.sar_val.value]
        else:
            reso = [self.picture_screen.ids.video_W.text,
                    self.picture_screen.ids.video_H.text]
        crop_width = self.picture_screen.ids.crop_W.text
        crop_height = self.picture_screen.ids.crop_H.text
        crop_top = self.picture_screen.ids.crop_T.text
        crop_bottom = self.picture_screen.ids.crop_B.text
        crop_right = self.picture_screen.ids.crop_R.text
        crop_left = self.picture_screen.ids.crop_L.text
        deteline = self.picture_screen.ids.deteline.text
        decomb = self.picture_screen.ids.decomb.text
        deinterlace = self.picture_screen.ids.deint.text
        denoise = self.picture_screen.ids.denoise.text

        return (reso, crop_width, crop_height, crop_top,
                crop_bottom, crop_right, crop_left,
                deteline, decomb, deinterlace, denoise)

    # Get video infos
    def get_video_infos(self):
        '''from data/mod_encode/screen/video.kv'''
        container = self.video_screen.ids.vcontainer.valueA
        codec = self.video_screen.ids.vcontainer.valueB

        if self.video_screen.ids.check_crf.active is True:
            crf = self.video_screen.ids.crf.value
            dual_pass = None
        else:
            crf = None
            dual_pass = self.video_screen.ids.video_bitrate.text
        framerate = self.video_screen.ids.fram_rate.text
        preset = self.video_screen.ids.pre_set.text
        tune = self.video_screen.ids.tu_ne.text
        profile = self.video_screen.ids.pro_file.text
        level = self.video_screen.ids.le_vel.text

        return (container, codec, crf, dual_pass,
                framerate, preset, tune, profile, level)

    # Get audio infos
    def get_audio_infos(self):
        '''from data/mod_encode/screen/widget/audio_track.kv'''
        [audio_ID, audio_title, audio_codec, audio_bitrate,
         audio_samplerate, audio_gain] = [[], [], [], [], [], []]
        layout = \
            self.audio_screen.ids.audio_track_layout.children

        for nb in range(0, len(layout)):
            audio_ID.append(layout[nb].ids.audio_track_ID.text)
            audio_title.append(layout[nb].ids.audio_track_title.text)
            audio_codec.append(layout[nb].ids.acodec.value)
            audio_bitrate.append(layoutn[nb].ids.abitrate.text)
            audio_samplerate.append(layout[nb].ids.sample_rate.text)
            audio_gain.append(layout[nb].ids.gain.text)
            nb = nb + 1

        return (audio_ID, audio_title, audio_codec,
                audio_bitrate, audio_samplerate, audio_gain)

    # Get subtitles infos
    def get_subtitles_infos(self):
        '''
        from data/mod_encode/screen/widget/sub_file.kv
        from data/mod_encode/screen/widget/sub_file.kv
        '''
        [subs_ID, subs_title, subs_forced, subs_burned, subs_default,
         subs_chars, subs_delay] = [[], [], [], [], [], [], []]
        layout = \
            self.subtitles_screen.ids.sub_track_layout.children

        for nb in range(0, len(layout)):
            subs_ID.append(layout[nb].ids.sub_track_ID.text)
            subs_title.append(layout[nb].ids.sub_track_title.text)
            subs_forced.append(layout[nb].ids.sub_forced.value)
            subs_burned.append(layout[nb].ids.sub_burned.value)
            subs_default.append(layout[nb].ids.sub_default.value)
            subs_chars.append(layout[nb].ids.sub_charset.text)
            subs_delay.append(layout[nb].ids.sub_delay.text)
            nb = nb + 1

        return (subs_ID, subs_title, subs_forced, subs_burned,
                subs_default, subs_chars, subs_delay)

    # Get advanced infos
    def get_advanced_infos(self):
        '''from data/mod_encode/screen/advanced.kv'''
        if self.advanced_screen.ids.threads_on.active is True:
            threads_nb = self.advanced_screen.ids.threads_nb.value
            threads_mod = self.advanced_screen.ids.threads_mod.value
        else:
            [threads_nb, threads_mod] = [None, ] * 2
        if self.advanced_screen.ids.frames_on.active is True:
            ref_frames = self.advanced_screen.ids.ref_frames.value
            max_Bframes = self.advanced_screen.ids.max_Bframes.value
            mixed_ref = self.advanced_screen.ids.mixed_ref.value
        else:
            [ref_frames, max_Bframes, mixed_ref] = [None, ] * 3
        if self.advanced_screen.ids.encod_on.active is True:
            pyramid_mod = self.advanced_screen.ids.pyram.text
            transform = self.advanced_screen.ids.transform.value
            cabac = self.advanced_screen.ids.cabac.value
        else:
            [pyramid_mod, transform, cabac] = [None, ] * 3
        if self.advanced_screen.ids.adapt_on.active is True:
            direct_mod = self.advanced_screen.ids.direct.text
            B_frames = self.advanced_screen.ids.Bframes.text
        else:
            [direct_mod, B_frames] = [None, ] * 2
        if self.advanced_screen.ids.weight_on.active is True:
            weighted_bf = self.advanced_screen.ids.weight_bf.text
            weighted_pf = self.advanced_screen.ids.weight_pf.value
        else:
            [weighted_bf, weighted_pf] = [None, ] * 2
        if self.advanced_screen.ids.motion_on.active is True:
            me_method = self.advanced_screen.ids.me_mod.text
            subpixel = self.advanced_screen.ids.subpixel.value
            me_range = self.advanced_screen.ids.me_range.value
        else:
            [me_method, subpixel, me_range] = [None, ] * 3
        if self.advanced_screen.ids.partitions_on.active is True:
            partitions = self.advanced_screen.ids.parts.text
            trellis = self.advanced_screen.ids.trell.text
        else:
            [partitions, trellis] = [None, ] * 2
        if self.advanced_screen.ids.quantiz_on.active is True:
            adapt_strenght = self.advanced_screen.ids.adapt_s.text
            psy_optim = self.advanced_screen.ids.psy_optim.value
        else:
            [adapt_strenght, psy_optim] = [None, ] * 2
        if self.advanced_screen.ids.distortion_on.active is True:
            distord_rate = self.advanced_screen.ids.dist_rate.text
            psy_trellis = self.advanced_screen.ids.psy_trell.text
        else:
            [distord_rate, psy_trellis] = [None, ] * 2
        if self.advanced_screen.ids.deblock_on.active is True:
            deblock_alpha = self.advanced_screen.ids.d_alpha.text
            deblock_beta = self.advanced_screen.ids.d_beta.text
        else:
            [deblock_alpha, deblock_beta] = [None, ] * 2
        if self.advanced_screen.ids.keyframe_on.active is True:
            key_interval = self.advanced_screen.ids.key_interval.text
            min_key = self.advanced_screen.ids.min_key.text
            lookahead = self.advanced_screen.ids.lookahead.text
        else:
            [key_interval, min_key, lookahead] = [None, ] * 3
        if self.advanced_screen.ids.various_on.active is True:
            scenecut = self.advanced_screen.ids.scenecut.text
            chroma = self.advanced_screen.ids.chroma.value
            fast_skip = self.advanced_screen.ids.fast_skip.value
            grayscale = self.advanced_screen.ids.grayscale.value
            bluray_compat = self.advanced_screen.ids.bluray_compat.value
        else:
            [scenecut, chroma, fast_skip,
             grayscale, bluray_compat] = [None, ] * 5

        return (
            threads_nb, threads_mod, ref_frames, max_Bframes,
            mixed_ref, pyramid_mod, transform, cabac, direct_mod,
            B_frames, weighted_bf, weighted_pf, me_method, subpixel,
            me_range, partitions, trellis, adapt_strenght, psy_optim,
            distord_rate, psy_trellis, deblock_alpha, deblock_beta,
            key_interval, min_key, lookahead, scenecut, chroma,
            fast_skip, grayscale, bluray_compat)

    # ---------------------------------------------------------------
    #  MANAGE ENCODE ################################################
    # ---------------------------------------------------------------
    '''Check and send content to app/mod_encode/manage.py'''

    # Check if user is not a n00b
    '''Essential values verification'''
    def check_encode_values(self):
        if self.source_screen.ids.r_source.active is True and\
                self.source_screen.ids.r_title.active is True and\
                (self.picture_screen.ids.auto_resize.active is True or\
                 self.picture_screen.ids.check_sar.active is True) and\
                self.video_screen.ids.check_codec.active is True:
            return True
        else:
            return False

if __name__ == '__main__':
    AnkoaApp().run()
