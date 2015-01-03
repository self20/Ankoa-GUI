#!/usr/bin/kivy
from kivy.uix.popup import Popup


def popup_error(error):
    from kivy.uix.rst import RstDocument
    popup = Popup(
        title='Warning', size_hint=(.3, .2),
        content=RstDocument(text=str(error)))
    popup.open()


class SettingsPopup(Popup):
    pass


class QueuePopup(Popup):
    pass


class ManagerPopup(Popup):
    pass


class HelpPopup(Popup):
    pass


class GithubPopup(Popup):
    pass


class AboutPopup(Popup):
    pass


class RemotePopup(Popup):
    pass


class ErrorPopup(Popup):
    pass


class ExitPopup(Popup):
    pass
