#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import kivy
kivy.require('1.8.0')
from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from os.path import dirname, join
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen
from kivy.properties import (NumericProperty, StringProperty,
                             ObjectProperty, ListProperty)
from app.mod_encode.bitrate_cal import *
from app.mod_encode.scan_source import *
from app.popup.popup_classes import *
from app.popup.settings import *

# SETTINGS
__version__ = 'Ankoa v0.1'
Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '768')
[count_audiotk, count_subtk] = [0, ] * 2


# INTERFACE
class AnkoaScreen(Screen):
    pass


# ANKOA
class AnkoaApp(App):

    # INTERACTIVE
    index = NumericProperty(-1)
    screen_names = ListProperty([])
    current_title = StringProperty()
    current_bitrate = StringProperty()
    scan_data = ObjectProperty()

    # LOAD USER SETTINGS
    (source_folder, dest_folder, team_name, tmdb_apikey, tk_announce,
     ssh_host, ssh_port, ssh_username, ssh_passwd, local_folder) =\
     load_settings()

    # BUILDER
    def build(self):
        self.title = __version__
        curdir = dirname(__file__)

        # MAIN SCREENS
        self.screens = {}
        self.menu_screens = sorted([
            'Encode', 'Remux', 'Extract', 'NFOgen',
            'Genprez', 'Thumbnails', 'Torrent'])
        self.screen_names = self.menu_screens
        self.menu_screens = [
            join(curdir, 'data', 'screen',
                 'mod_{}.kv'.format(fn)) for fn in self.menu_screens]
        self.go_next_screen()

    # RESTART ANKOA
    def restart_ankoa(self):
        restart = sys.executable
        os.execl(restart, restart, * sys.argv)

    # MANAGE MAIN SCREENS
    def go_previous_screen(self):
        self.index = (self.index - 1) % len(self.menu_screens)
        screen = self.load_screen(self.index)
        header_screens = self.root.ids.header_screens
        header_screens.switch_to(screen, direction='right')
        self.current_title = screen.name

    def go_next_screen(self):
        self.index = (self.index + 1) % len(self.menu_screens)
        screen = self.load_screen(self.index)
        header_screens = self.root.ids.header_screens
        header_screens.switch_to(screen, direction='left')
        self.current_title = screen.name

    def go_screen(self, current_screen):
        self.index = current_screen
        screen = self.load_screen(self.index)
        self.root.ids.header_screens.switch_to(
            self.load_screen(current_screen), direction='left')
        self.current_title = screen.name

    def load_screen(self, index):
        if index in self.screens:
            return self.screens[index]
        screen = Builder.load_file(self.menu_screens[index].lower())
        self.screens[index] = screen
        return screen

    # MANAGE ENCODE SCREENS
    for mod_encod_kvs in os.listdir('data/screen/mod_encode/'):
        if mod_encod_kvs.endswith('.kv'):
            Builder.load_file(
                'data/screen/mod_encode/{}'.format(mod_encod_kvs))

    # MANAGE POPUPS
    for popup in os.listdir('data/popup/'):
        if popup.endswith('.kv'):
            Builder.load_file('data/popup/{}'.format(popup))

    def main_popup(self, popup_id):
        popup = '{}'.format(popup_id)
        eval(popup).open()

    # MANAGE VIDEO TRACKS
    def scan_source_infos(self, source):
        (self.scan_data) = scan_source(source)

    def toggle_bitrate(self, state):
        if state == 'down':
            height = 50
        else:
            height = 0
        Animation(height=height, d=.3, t='out_quart').start(
            self.root.ids.header_screens.current_screen
            .ids.video.ids.bitrate_view)

    def bit_calculator(self, HH, MM, SS, audio_bit, desired_size):
        current_bitrate = calculator(HH, MM, SS, audio_bit, desired_size)
        self.current_bitrate = str(current_bitrate)
        return self.current_bitrate

    # MANAGE AUDIO TRACKS
    def audioTrack(self, request):
        global count_audiotk

        audio_track = Builder.load_file(
            'data/screen/mod_encode/widget/audio_track.kv')
        track_layout = self.root.ids.header_screens\
            .current_screen.ids.audio.ids.audio_track_layout

        if request == 'add_track' and count_audiotk < 5:
            track_layout.add_widget(audio_track)
            count_audiotk += 1

        elif request == 'clear_tracks':
            track_layout.clear_widgets()
            count_audiotk = 0

        elif request == 'del_track':
            track_layout.remove_widget(track_layout.children[-1])
            if count_audiotk > 0:
                count_audiotk += -1
        else:
            pass

    # MANAGE SUBTITLES TRACKS
    def subtitlesTrack(self, request):
        global count_subtk

        sub_track = Builder.load_file(
            'data/screen/mod_encode/widget/sub_track.kv')
        sub_file = Builder.load_file(
            'data/screen/mod_encode/widget/sub_file.kv')
        track_layout = self.root.ids.header_screens\
            .current_screen.ids.subtitles.ids.sub_track_layout

        if request == 'add_track' and count_subtk < 7:
            count_subtk += 1
            track_layout.add_widget(sub_track)

        elif request == 'add_file_track' and count_subtk < 7:
            count_subtk += 1
            track_layout.add_widget(sub_file)

        elif request == 'clear_tracks':
            track_layout.clear_widgets()
            count_subtk = 0

        elif request == 'del_track':
            track_layout.remove_widget(track_layout.children[-1])
            if count_subtk > 0:
                count_subtk += -1
        else:
            pass

    # MANAGE SETTINGS
    def save_settings(self, source_folder, dest_folder, team_name,
                      tmdb_apikey, tk_announce, ssh_host, ssh_port,
                      ssh_username, ssh_passwd, local_folder, request):

        modify_settings(source_folder, dest_folder, team_name,
                        tmdb_apikey, tk_announce, ssh_host, ssh_port,
                        ssh_username, ssh_passwd, local_folder)

    def reset_settings(self):
        clear_settings()

if __name__ == '__main__':
    AnkoaApp().run()
