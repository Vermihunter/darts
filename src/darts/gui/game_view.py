# game_view.py
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from .darts_board import DartsBoard
from .score_area import ScoreAreaTop, ScoreAreaBottom


@Gtk.Template(resource_path="/com/vermesa/darts/ui/game_view.ui")
class GameView(Gtk.Box):
    __gtype_name__ = "GameView"

    board = Gtk.Template.Child() 
    outer_paned = Gtk.Template.Child()
    right_paned = Gtk.Template.Child()
    
    score_top = Gtk.Template.Child()
    score_bottom = Gtk.Template.Child()
    
    
    
    def __init__(self):
        super().__init__()

        # set initial split positions (pixels)
        self.outer_paned.set_position(1000)
        self.right_paned.set_position(500)
        self.board.connect("throw", self.on_throw)
        self.curr_score = self.score_top
        self.other_score = self.score_bottom
        self.curr_throws = []

    def on_throw(self, board, ring, base, score):
        print("HIT:", ring, base, score)
        
        if ring == "OUTER BULL":
            throw = "25"
        elif ring == "DOUBLE":
            throw = f"D{base}"
        elif ring == "TRIPLE":
            throw = f"T{base}"
        elif ring == "INNER BULL":
            throw = "BULL"
        elif ring == "MISS":
            throw = "MISS"
        else:
            throw = str(base)
        
        
        
        self.curr_throws.append(throw)
        
        if len(self.curr_throws) == 3:
            self.curr_score.add_round(self.curr_throws)
            self.curr_throws = []
            # Swapping
            self.curr_score, self.other_score = self.other_score, self.curr_score