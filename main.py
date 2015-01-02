#!/usr/bin/kivy
__date__ = '2014 * 2015'
__version__ = 'Ankoa v0.1'
__author__ = 'grm34@FRIPOUILLEJACK'
__license__ = 'CeCILL-C Free Software'
__copyright__ = 'https://github.com/Ankoa'

# Python libraries
import os
import sys
import platform
import subprocess
from os.path import (dirname, join)

# Kivy libraries
import kivy
kivy.require('1.8.0')
from kivy.app import App
from kivy.compat import PY2
from kivy.lang import Builder
from kivy.config import Config
from kivy.animation import Animation
from kivy.core.clipboard import Clipboard
from kivy.properties import (
    NumericProperty, StringProperty,
    ObjectProperty, ListProperty)

# Local libraries
from app.settings.config import (
    load_session, modify_session,
    clear_session, load_settings,
    modify_settings, clear_settings)
from app.mod_encode.encode_man import (
    manage_video, manage_audio, manage_subs,
    manage_advanced, build_advanced, manage_ffmpeg)
from app.mod_encode.encode_dict import (o_o, error)
from app.mod_encode.bitrate_calc import calculator
from app.screen.screens import AnkoaScreen
from app.settings.conf_dict import user
from app.scan.scan_source import scan
from app.server.remote import remote
from app.popup.popups import *


class AnkoaApp(App):

    # MANAGE EVENTS
    # ===============================================================
    ''' Here we use kivy properties to define events and bind to
    them. Properties produce events such that when an attribute of
    one object changes, all properties that reference that attribute
    are automatically updated. '''

    # General
    current_track = ObjectProperty()
    current_error = StringProperty()

    # Screens
    index = NumericProperty(-1)
    screen_names = ListProperty([])
    current_title = StringProperty()

    # Encode Mode
    current_bitrate = StringProperty()
    scan_encode = ObjectProperty()
    encode_source = StringProperty()
    audio_count = NumericProperty(0)
    sub_count = NumericProperty(0)

    # Remux Mode
    scan_remux = ObjectProperty()
    remux_source = StringProperty()
    track_count = NumericProperty(0)

    # Extract Mode
    scan_extract = ObjectProperty()
    extract_source = StringProperty()

    # APPLICATION ROOT
    # ===============================================================
    ''' Here we use build method to define application configuration,
    settings and to initialize our graphic environment. The root
    application is created from the corresponding .kv (ankoa.kv). '''

    def build_config(self, config):

        # Set app resolution
        Config.set('graphics', 'width', '1024')
        Config.set('graphics', 'height', '768')

        # Load user settings & session
        use_kivy_settings = False
        load_settings()
        if 'Linux' in platform.system():
            load_session()

    def build(self):

        # Set app title
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

        # Display 1st screen on start
        self.go_next_screen()

        # Get ENCODE_MODE Layouts
        self.source_enc = \
            self.root.ids.header_screens.current_screen.ids.source_enc
        self.picture_enc = \
            self.root.ids.header_screens.current_screen.ids.picture_enc
        self.video_enc = \
            self.root.ids.header_screens.current_screen.ids.video_enc
        self.audio_enc = \
            self.root.ids.header_screens.current_screen.ids.audio_enc
        self.subtitles_enc = \
            self.root.ids.header_screens.current_screen.ids.subtitles_enc
        self.advanced_enc = \
            self.root.ids.header_screens.current_screen.ids.advanced_enc
        self.queue_enc = \
            self.root.ids.header_screens.current_screen.ids.queue_enc

    # USER SETTINGS
    # ===============================================================
    ''' User settings management: function to check if settings are
    defined, another to save them and another one to clear them. '''

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

    # USER SESSION
    # ===============================================================
    ''' User session management: function to check if session is
    defined, another to save them and another one to clear them.
    Remote session management: function to launch proper sshfs
    session for current user plateform.'''

    # Save user session
    def save_session(self):
        modify_session()

    # Clear user session
    def reset_session(self):
        clear_session()

    # Unix session
    def manage_remote(self, request):
        remote(request)

    # Windows session
    def run_sshfs_win(self):
        subprocess.call('contrib\sshfs\win\DokanSSHFS.exe')

    # UTILITIES
    # ===============================================================
    ''' Some global utilities such as restart the application, copy
    something to clipboard on demand, get current track layout, ... '''

    # Restart App
    def restart_ankoa(self):
        restart = sys.executable
        os.execl(restart, restart, * sys.argv)

    # Copy to clipboard
    def copy_to_clipboard(self, text):
        Clipboard.put(bytes(text, 'UTF-8'), 'UTF8_STRING')
        Clipboard.get('UTF8_STRING')

    # Get current track layout
    def get_current_track(self, current_track):
        self.current_track = current_track
        return self.current_track

    # MANAGE POPUPS
    # ===============================================================
    ''' Here we load all popups on start (kv files) and we use a
    function to easy display them on demand, with a simple request. '''

    # Load popups
    for popup in os.listdir('data/popup/'):
        if popup.endswith('.kv'):
            Builder.load_file('data/popup/{}'.format(popup))

    # Display popups
    def main_popup(self, popup_id):
        ''' Function to display popups. It call corresponding class
        in app.popup.popups from anywhere with current popup_id. '''

        popup = '{}'.format(popup_id)
        eval(popup).open()

    # MANAGE SCREENS
    # ===============================================================
    ''' We previously created one screen per mode, those functions
    will display them on demand (previous/next or selection). '''

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

    # MANAGE SCREENS LAYOUTS
    # ===============================================================
    ''' Here we just load all layouts, they are the windows of
    one screen. Each mode contains it own screen that contains
    it's own layouts, so let's load them separatly. '''

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

    # MANAGE VIDEO SOURCES
    # ===============================================================
    ''' Functions to load or scan a video on filemanager selection.
    We simply use requests to define the mode which asking for. '''

    # Scan video source
    def scan_source_infos(self, source):
        ''' Function will return a complete mediainfo with
        autocrop values. It call app.scan.scan_source.scan. '''

        if user['request'] == 'encode_source':
            self.scan_encode = scan(source)
        elif user['request'] == 'remux_source':
            self.scan_remux = scan(source)
        elif user['request'] == 'extract_source':
            self.scan_extract = scan(source)

    # Load Video Source
    def load_video_source(self, source):
        ''' Function to get source location on filemanager
        selection. Also required by the video player preview. '''

        if user['request'] == 'encode_source':
            self.encode_source = source
        elif user['request'] == 'remux_source':
            self.remux_source = source
        elif user['request'] == 'extract_source':
            self.extract_source = source

    # MODE ENCODE: VIDEO LAYOUT
    # ===============================================================
    ''' Video bitrate calculator functions. Animation to display
    bitrate calculator interface and one function for calculate. '''

    # Video bitrate layout
    def toggle_bitrate(self, state):
        ''' Toggle bitrate row animation (row height on/off)
        from data.screen.mod_encode.video_enc [Bitrate button]. '''

        if state == 'down':
            height = 42
        else:
            height = 0
        Animation(height=height, d=.1, t='out_quart').start(
            self.video_enc.ids.bitrate_view)

    # Video bitrate calculator
    def bit_calculator(self):
        ''' Function will return video bitrate in Kbps.
        It call app.mod_encode.bitrate_calculator from
        data.screen.mod_encode.video_enc [RUN button].'''

        current_bitrate = calculator()
        self.current_bitrate = str(current_bitrate)
        return self.current_bitrate

    # MODE ENCODE: AUDIO LAYOUT
    # ===============================================================
    ''' Audio tracks management. Here we add/del tracks such as
    widgets on demand. The limitation is to 10 tracks. '''

    # Get Audio Track parent
    def get_audioTrack_enc(self):
        track_layout = self.audio_enc.ids.audio_track_layout
        return track_layout

    # Add Audio Track
    def add_audioTrack_enc(self):
        if self.audio_count < 10:
            track_layout = self.get_audioTrack_enc()
            track = Builder.load_file(
                'data/screen/mod_encode/widget/audioTrack_enc.kv')
            track_layout.add_widget(track)
            self.audio_count += 1

    # Delete current Audio Track
    def del_audioTrack_enc(self, current_track):
        track_layout = self.get_audioTrack_enc()
        track_layout.remove_widget(current_track)
        if self.audio_count > 0:
            self.audio_count += -1

    # Clear all Audio Tracks
    def clear_audioTracks_enc(self):
        track_layout = self.get_audioTrack_enc()
        track_layout.clear_widgets()
        self.audio_count = 0

    # MODE ENCODE: SUBTITLES LAYOUT
    # ===============================================================
    ''' Subtitles tracks management. Here we add/del tracks such
    as widgets on demand. The limitation is to 10 tracks. '''

    # Get Subtitles Tracks parent
    def get_subTrack_enc(self):
        track_layout = self.subtitles_enc.ids.sub_track_layout
        return track_layout

    # Add Subtitles Track
    def add_subTrack_enc(self, request):
        if self.sub_count < 10:
            track_layout = self.get_subTrack_enc()
            track = Builder.load_file(
                'data/screen/mod_encode/widget/{}_enc.kv'
                .format(request))
            track_layout.add_widget(track)
            self.sub_count += 1

    # Delete current Subtitles Track
    def del_subTrack_enc(self, current_track):
        track_layout = self.get_subTrack_enc()
        track_layout.remove_widget(current_track)
        if self.sub_count > 0:
            self.sub_count += -1

    # Clear all Subtitles Tracks
    def clear_subTracks_enc(self):
        track_layout = self.get_subTrack_enc()
        track_layout.clear_widgets()
        self.sub_count = 0

    # Load Subtitles File Source
    def load_subSource_enc(self, value):
        ''' Function to get subfile location on filemanager
        selection to display subfile title in corresponding
        track area. '''

        current_track = self.get_current_track(self.current_track)
        current_track.ids.sub_source.text = value.split('/')[-1]
        current_track.ids.sub_codec.value = value.split('.')[-1]

    # MODE ENCODE: MANAGEMENT
    # ===============================================================
    ''' Here is recovered current encode settings to send them to the
    manager, it will return ffmpeg command line. In case of local
    usage, this command will be executed localy, or sent to a
    remote server. Queue mode is not already built. '''

    # Get user entries
    def get_encode_infos(self):
        ''' Function to get encode values from corresponding layout
        and to fill them in encode dictionary o_o.'''

        # Get source infos
        o_o['rls_source'] = self.source_enc.ids.source.text
        o_o['rls_title'] = self.source_enc.ids.title.text

        # Get picture infos
        if self.picture_enc.ids.check_sar.active is True:
            o_o['sar'] = self.picture_enc.ids.sar_val.value
        else:
            o_o['resolution'] = '{0}x{1}'.format(
                self.picture_enc.ids.video_W.text,
                self.picture_enc.ids.video_H.text)
        if self.picture_enc.ids.custom_crop.active is True:
            o_o['crop_width'] = self.picture_enc.ids.crop_W.text
            o_o['crop_height'] = self.picture_enc.ids.crop_H.text
            o_o['crop_right_left'] = self.picture_enc.ids.crop_R.text
            o_o['crop_top_bottom'] = self.picture_enc.ids.crop_T.text
        o_o['deinterlace'] = self.picture_enc.ids.deint.text
        o_o['motion_deint'] = self.picture_enc.ids.motion_d.text
        o_o['denoise'] = self.picture_enc.ids.denoise.text
        o_o['decimate'] = self.picture_enc.ids.decimate.text

        # Get video infos
        o_o['video_ID'] = self.video_enc.ids.video_track_ID.text
        o_o['movie_name'] = self.video_enc.ids.movie_name.text
        o_o['container'] = self.video_enc.ids.vcontainer.valueA
        o_o['video_codec'] = self.video_enc.ids.vcontainer.valueB
        if self.video_enc.ids.check_crf.active is True:
            o_o['crf_mode'] = self.video_enc.ids.crf_val.text
        else:
            o_o['dual_pass'] = self.video_enc.ids.video_bitrate.text
            o_o['fast1pass'] = self.video_enc.ids.fast1pass.value
        o_o['framerate'] = self.video_enc.ids.fram_rate.text
        o_o['preset'] = self.video_enc.ids.pre_set.value
        o_o['tune'] = self.video_enc.ids.tu_ne.value
        o_o['profile'] = self.video_enc.ids.pro_file.text
        o_o['level'] = self.video_enc.ids.le_vel.text

        # Get audio infos
        audio = self.audio_enc.ids.audio_track_layout.children[::-1]
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
        sub = self.subtitles_enc.ids.sub_track_layout.children[::-1]
        for nb in range(0, len(sub)):
            o_o['subs_type'].append(sub[nb].ids.sub_infos.type)
            o_o['subs_source'].append(sub[nb].ids.sub_source.text)
            o_o['subs_codec'].append(sub[nb].ids.sub_codec.value)
            o_o['subs_lang'].append(sub[nb].ids.sub_track_lang.text)
            o_o['subs_forced'].append(sub[nb].ids.sub_forced.value)
            o_o['subs_burned'].append(sub[nb].ids.sub_burned.value)
            o_o['subs_charset'].append(sub[nb].ids.sub_charset.text)

        # Get advanced infos
        if self.advanced_enc.ids.threads_on.active is True:
            o_o['threads_nb'] = self.advanced_enc.ids.threads.text
            o_o['threads_mod'] = self.advanced_enc.ids.threads_mod.value
        if self.advanced_enc.ids.frames_on.active is True:
            o_o['ref_frames'] = self.advanced_enc.ids.ref_frames.text
            o_o['max_Bframes'] = self.advanced_enc.ids.max_Bframes.text
            o_o['mixed_ref'] = self.advanced_enc.ids.mixed_ref.value
        if self.advanced_enc.ids.encod_on.active is True:
            o_o['pyramid_mod'] = self.advanced_enc.ids.pyram.value
            o_o['transform'] = self.advanced_enc.ids.transform.value
            o_o['cabac'] = self.advanced_enc.ids.cabac.value
        if self.advanced_enc.ids.adapt_on.active is True:
            o_o['direct_mod'] = self.advanced_enc.ids.direct.value
            o_o['B_frames'] = self.advanced_enc.ids.Bframes.value
        if self.advanced_enc.ids.weight_on.active is True:
            o_o['weighted_pf'] = self.advanced_enc.ids.weight_pf.value
            o_o['weighted_bf'] = self.advanced_enc.ids.weight_bf.value
        if self.advanced_enc.ids.motion_on.active is True:
            o_o['me_method'] = self.advanced_enc.ids.me_mod.text
            o_o['subpixel'] = self.advanced_enc.ids.subpixel.text
            o_o['me_range'] = self.advanced_enc.ids.me_range.text
        if self.advanced_enc.ids.partitions_on.active is True:
            o_o['partitions'] = self.advanced_enc.ids.parts.text
            o_o['trellis'] = self.advanced_enc.ids.trellis.value
        if self.advanced_enc.ids.quantiz_on.active is True:
            o_o['adapt_strenght'] = self.advanced_enc.ids.adapt_s.text
            o_o['psy_optim'] = self.advanced_enc.ids.psy_optim.value
        if self.advanced_enc.ids.distortion_on.active is True:
            o_o['distord_rate'] = self.advanced_enc.ids.dist_rate.text
            o_o['psy_trellis'] = self.advanced_enc.ids.psy_trell.text
        if self.advanced_enc.ids.deblock_on.active is True:
            o_o['deblock_alpha'] = self.advanced_enc.ids.d_alpha.text
            o_o['deblock_beta'] = self.advanced_enc.ids.d_beta.text
        if self.advanced_enc.ids.keyframe_on.active is True:
            o_o['key_interv'] = self.advanced_enc.ids.key_interval.text
            o_o['min_key'] = self.advanced_enc.ids.min_key.text
            o_o['lookahead'] = self.advanced_enc.ids.lookahead.text
        if self.advanced_enc.ids.various_on.active is True:
            o_o['scenecut'] = self.advanced_enc.ids.scenecut.text
            o_o['chroma'] = self.advanced_enc.ids.chroma.value
            o_o['fast_skip'] = self.advanced_enc.ids.fast_skip.value
            o_o['grayscale'] = self.advanced_enc.ids.grayscale.value
            o_o['bluray'] = self.advanced_enc.ids.bluray_compat.value

    # Essential content verification
    def check_encode_values(self):
        ''' Here we check if nothing is missing. One error will
        be displayed in a popup in case of missing values. '''

        if self.check_user_settings() is True and\
                self.source_enc.ids.r_source.active is True and\
                self.source_enc.ids.r_title.active is True and\
                (self.picture_enc.ids.reso.active is True or
                 self.picture_enc.ids.check_sar.active is True) and\
                self.video_enc.ids.check_vtrack.active is True and\
                self.video_enc.ids.check_codec.active is True:
            return True
        else:
            if self.check_user_settings() is False:
                self.current_error = error['settings']
            elif self.source_enc.ids.r_source.active is False:
                self.current_error = error['source']
            elif self.source_enc.ids.r_title.active is False:
                self.current_error = error['title']
            elif self.picture_enc.ids.reso.active is False or\
                    self.picture_enc.ids.check_sar.active is False:
                self.current_error = error['reso']
            elif self.video_enc.ids.check_vtrack.active is False:
                self.current_error = error['video']
            elif self.video_enc.ids.check_codec.active is False:
                self.current_error = error['codec']
            return False

    # Reset dictionary o_o
    def reset_dictionary(self):
        self.queue_enc.ids.ffmpeg_cmd.text = ''
        for key, value in o_o.items():
            if isinstance(value, list):
                o_o[key] = []
            else:
                o_o[key] = ''

    # Send content
    def send_encode_values(self):
        ''' Function to send content to the manager.
        Manager will return ffmpeg command line. We also
        print this command in corresponding area. '''

        self.get_encode_infos()
        manage_video()
        manage_audio()
        manage_subs()
        manage_advanced()
        build_advanced()
        manage_ffmpeg()
        self.queue_enc.ids.ffmpeg_cmd.text = '{}'.format(o_o['ffmpeg'])

        ''' debug '''
        print (str(o_o).replace(", ", "'\n")
                       .replace("],", "]\n"))

    # MODE REMUX: TRACKS LAYOUT
    # ===============================================================
    ''' Audio & subtitles tracks management. Here we add/del tracks
    such as widgets on demand. The limitation is to 10 tracks. '''

    # Get Track parent
    def get_Track_rmx(self):
        track_layout = \
            self.root.ids.header_screens.current_screen\
            .ids.tracks_rmx.ids.tracks_layout_rmx
        return track_layout

    # Add Track
    def add_Track_rmx(self, request):
        if self.track_count < 10:
            track_layout = self.get_Track_rmx()
            track = Builder.load_file(
                'data/screen/mod_remux/widget/{}_rmx.kv'
                .format(request))
            track_layout.add_widget(track)
            self.track_count += 1

    # Delete current Track
    def del_Track_rmx(self, current_track):
        track_layout = self.get_Track_rmx()
        track_layout.remove_widget(current_track)
        if self.track_count > 0:
            self.track_count += -1

    # Clear Tracks
    def clear_Tracks_rmx(self):
        track_layout = self.get_Track_rmx()
        track_layout.clear_widgets()
        self.track_count = 0

if __name__ == '__main__':
    AnkoaApp().run()
