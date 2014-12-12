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
from app.mod_encode.manager import encode_manager
from app.mod_encode.encode_dict import o_o
from app.mod_encode.bitrate_cal import *
from app.mod_encode.scan_source import *
from app.popup.popup_classes import *
from app.settings.settings import *
from app.server.remote import *

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
        self.queue_screen = \
            self.root.ids.header_screens.current_screen.ids.queue

    # ---------------------------------------------------------------
    #  SETTINGS #####################################################
    # ---------------------------------------------------------------

    # Load user settings on start
    '''call app.popup.settings: load_settings()'''
    (source_folder, dest_folder, team_name, tmdb_apikey,
     tk_announce, ssh_host, ssh_port, ssh_username,
     ssh_passwd, remote_folder) = load_settings()

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
            height = 42
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
        current_track.ids.sub_source.text = value.split('/')[-1]
        current_track.ids.sub_codec.value = value.split('.')[-1]

    # ---------------------------------------------------------------
    #  MAPPING ENCODE ###############################################
    # ---------------------------------------------------------------

    # Get encode infos
    def get_encode_infos(self, o_o):
        '''
        Get all screens values from corresponding kv file
        Fill in the dictionary o_o
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
            o_o['threads_nb'] = self.advanced_screen.ids.threads_nb.value
            o_o['threads_mod'] = self.advanced_screen.ids.threads_mod.value
        if self.advanced_screen.ids.frames_on.active is True:
            o_o['ref_frames'] = self.advanced_screen.ids.ref_frames.value
            o_o['max_Bframes'] = self.advanced_screen.ids.max_Bframes.value
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
            o_o['subpixel'] = self.advanced_screen.ids.subpixel.value
            o_o['me_range'] = self.advanced_screen.ids.me_range.value
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
    '''
    Check content and call the manager 'app/mod_encode/manager.py'
    Manager will return proper FFMPEG cmd
    '''

    # Check if user is not a n00b
    '''Essential content verification'''
    def check_encode_values(self):
        if self.source_screen.ids.r_source.active is True and\
                self.source_screen.ids.r_title.active is True and\
                (self.picture_screen.ids.reso.active is True or
                 self.picture_screen.ids.check_sar.active is True) and\
                self.video_screen.ids.check_vtrack.active is True and\
                self.video_screen.ids.check_codec.active is True:
            return True
        else:
            return False

    # Reset dictionary
    def reset_dictionary(self):
        self.queue_screen.ids.ffmpeg_cmd.text = ''
        for key, value in o_o.items():
            if isinstance(value, list):
                o_o[key] = []
            else:
                o_o[key] = ''

    # Get content and call the Manager
    def send_encode_values(self):
        self.get_encode_infos(o_o)
        ffmpeg = encode_manager(o_o, self.team_name, self.dest_folder)
        self.queue_screen.ids.ffmpeg_cmd.text = '{}'.format(ffmpeg)

        '''debug'''
        print (str(o_o).replace(", ", "'\n")
                       .replace("],", "]\n"))

if __name__ == '__main__':
    AnkoaApp().run()
