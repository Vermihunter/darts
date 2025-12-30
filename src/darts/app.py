import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio

res = Gio.Resource.load("data/resources/resources.gresource")
Gio.resources_register(res)

from .gui.darts_board import DartsBoard
from .gui.game_view import GameView



def main():
    app = Gtk.Application(application_id="com.vermesa.darts")
    app.connect("activate", on_activate)
    app.run(None)

def on_activate(app):
    window = Gtk.ApplicationWindow(application=app, title="Darts Simulator")
    view = GameView()
    window.set_child(view)
    window.set_default_size(1920, 1080)   # width, height

    window.present()
