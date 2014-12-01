#!/usr/bin/python
# -*- coding: utf-8 -*-
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

# Load required scripts
from app.mod_encode.bitrate_cal import *
from app.mod_encode.scan_source import *
from app.popup.popup_classes import *
from app.popup.settings import *
from app.popup.remote import *

# Interface Resolution
Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '768')

# Set Tracks count variables
[count_audiotk, count_subtk] = [0, ] * 2


# CONTAINER (principal screen)
class AnkoaScreen(Screen):
    pass


# Ankoa-GUI
class AnkoaApp(App):

    # Set variables property (required in kv files)
    index = NumericProperty(-1)
    screen_names = ListProperty([])
    current_title = StringProperty()
    current_bitrate = StringProperty()
    scan_data = ObjectProperty()

    # Load user settings [call app.popup.settings: load_settings()]
    (source_folder, dest_folder, team_name, tmdb_apikey, tk_announce,
     ssh_host, ssh_port, ssh_username, ssh_passwd,
     remote_folder) = load_settings()

    # Ankoa Root
    def build(self):
        self.title = __version__
        self.screens = {}

        # Set screens names
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

    # Load corresponding screen on request
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

    # Scan video source
    def scan_source_infos(self, source):
        '''
            Call app.mod_encode.scan_source.py: scan()
            From data.screen.mod_encode.source.kv [scan button]
        '''
        self.scan_data = scan_source(source)

    # Video bitrate calculator section
    def toggle_bitrate(self, state):
        '''
            Toggle bitrate row animation (row height on/off)
            From data.screen.mod_encode.video.kv [Bitrate button]
        '''
        if state == 'down':
            height = 50
        else:
            height = 0
        Animation(height=height, d=.3, t='out_quart').start(
            self.root.ids.header_screens.current_screen
            .ids.video.ids.bitrate_view)

    # Video bitrate calculator action
    def bit_calculator(self, HH, MM, SS, audio_bit, desired_size):
        '''
            Call app.mod_encode.bitrate_cal.py: calculator()
            From data.screen.mod_encode.video.kv [RUN button]
        '''
        current_bitrate = calculator(HH, MM, SS, audio_bit, desired_size)
        self.current_bitrate = str(current_bitrate)
        return self.current_bitrate

    # Audio Tracks
    def audioTrack(self, request):
        global count_audiotk
        '''
            Manage audio Tracks screen
            From data.screen.mod_encode.audio.kv
        '''

        # Load audio Track Layout (kv file)
        audio_track = Builder.load_file(
            'data/screen/mod_encode/widget/audio_track.kv')
        track_layout = self.root.ids.header_screens\
            .current_screen.ids.audio.ids.audio_track_layout

        # Add audio Track (max 5 tracks)
        if request == 'add_track' and count_audiotk < 5:
            track_layout.add_widget(audio_track)
            count_audiotk += 1

        # Clear all audio Tracks
        elif request == 'clear_tracks':
            track_layout.clear_widgets()
            count_audiotk = 0

        # Delete selected audio Track
        elif request == 'del_track':
            track_layout.remove_widget(track_layout.children[-1])
            if count_audiotk > 0:
                count_audiotk += -1
        else:
            pass

    # Subtitles Tracks
    def subtitlesTrack(self, request):
        global count_subtk
        '''
            Manage subtitles Tracks screen
            From data.screen.mod_encode.subtitles.kv
        '''

        # Load sub Track Layouts (kv files)
        sub_track = Builder.load_file(
            'data/screen/mod_encode/widget/sub_track.kv')
        sub_file = Builder.load_file(
            'data/screen/mod_encode/widget/sub_file.kv')
        track_layout = self.root.ids.header_screens\
            .current_screen.ids.subtitles.ids.sub_track_layout

        # Add subtitles Track from source (max 7)
        if request == 'add_track' and count_subtk < 7:
            count_subtk += 1
            track_layout.add_widget(sub_track)

        # Add subtitles Track from file (max 7)
        elif request == 'add_file_track' and count_subtk < 7:
            count_subtk += 1
            track_layout.add_widget(sub_file)

        # Clear all subtitles Tracks
        elif request == 'clear_tracks':
            track_layout.clear_widgets()
            count_subtk = 0

        # Delete selected subtitles Track
        elif request == 'del_track':
            track_layout.remove_widget(track_layout.children[-1])
            if count_subtk > 0:
                count_subtk += -1
        else:
            pass

if __name__ == '__main__':
    AnkoaApp().run()
