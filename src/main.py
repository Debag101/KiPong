from kivy.app import App
from kivy.lang import Builder

from screens.game_screen import GameWindow

class KiPong(App):

    title = 'KiPong - Pong Game'

    def build(self):
        kv = Builder.load_file('../design/style.kv')
        return kv
    
KiPong().run()