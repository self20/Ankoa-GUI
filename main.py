#!/usr/bin/kivy
import os
from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from os.path import dirname, join
from kivy.animation import Animation
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.properties import (NumericProperty, StringProperty, ListProperty)
from app.popup.main_popup import *

# INTERFACE SETTINGS
Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '768')
count = 0


# MAIN INTERFACE
class AnkoaScreen(Screen):
    pass


# MAIN APP
class AnkoaApp(App):

    # INTERACTIVE CONTENT
    index = NumericProperty(-1)
    current_title = StringProperty()
    screen_names = ListProperty([])

    # BUILDER
    def build(self):
        self.title = 'AnkoA v1.0.1'
        curdir = dirname(__file__)

        # BUILD MAIN SCREENS
        self.screens = {}
        self.menu_screens = sorted([
            'Encode', 'Remux', 'Extract', 'NFOgen',
            'Genprez', 'Thumbnails', 'Torrent'])
        self.screen_names = self.menu_screens
        self.menu_screens = [
            join(curdir, 'data', 'screen',
                 'mod_{}.kv'.format(fn)) for fn in self.menu_screens]
        self.go_next_screen()

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

    # ENCODE MODE SCREENS
    for mod_encod_kvs in os.listdir('data/screen/mod_encode/'):
        if mod_encod_kvs.endswith('.kv'):
            Builder.load_file(
                'data/screen/mod_encode/{}'.format(mod_encod_kvs))

    # MANAGE POPUPS
    Builder.load_file('data/popup/main_popup.kv')
    def main_popup(self, popup_id):
        popup = '{}'.format(popup_id)
        eval(popup).open()

    # MANAGE VIDEO TRACKS
    def toggle_bitrate(self, state):
        if state == 'down':
            height = 50
        else:
            height = 0
        Animation(height=height, d=.3, t='out_quart').start(
            self.root.ids.header_screens.current_screen
            .ids.video.ids.bitrate_view)

    # MANAGE AUDIO TRACKS
    def audioTrack(self, request):
        global count
        audio_track = Builder.load_file(
            'data/screen/mod_encode/widget/audio_track.kv')
        track_layout = self.root.ids.header_screens\
            .current_screen.ids.audio.ids.audio_track_layout
        if request == 'add_track' and count < 5:
            count += 1
            track_layout.add_widget(audio_track)
        elif request == 'del_track':
            track_layout.remove_widget(audio_track)
            count -= 1
        elif request == 'clear_tracks':
            track_layout.clear_widgets(audio_track)
            count = 0

if __name__ == '__main__':
    AnkoaApp().run()
