# score_area.py
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
from .round_renderer import RoundRenderer


class BaseScoreArea(Gtk.DrawingArea):
    def __init__(self, color):
        super().__init__()
        self.rounds = []     # e.g. ["T20", "5", "D10"]
        self.color = color
        self.set_content_width(200)
        self.set_content_height(150)
        self.set_draw_func(self.on_draw)
        

    
    def add_round(self, throws):
        number = len(self.rounds) + 1
        self.rounds.append(RoundRenderer(number, throws))
        self.queue_draw()

    def on_draw(self, area, cr, w, h):
        cr.set_source_rgb(*self.color)
        cr.paint()

        cr.set_source_rgb(0,0,0)
        cr.rectangle(5,5,w-10,h-10)
        cr.stroke()
        
        y = 25
        cr.set_font_size(16)

        for r in self.rounds:
            _, height = r.layout(cr)
            r.draw(cr, 10, y)
            y += height + 14   

        # for round_index, t in enumerate(self.throws, start=1):

        #     # --- 1️⃣ prefix text --- 
        #     prefix = f"ROUND {round_index} →  "

        #     x = 10
        #     cr.move_to(x, y)
        #     cr.show_text(prefix)

        #     # --- 2️⃣ measure it ---
        #     ext = cr.text_extents(prefix)
        #     x += ext.x_advance   # <-- throws start after prefix

        #     # --- 3️⃣ draw throws for this round ---
        #     for throw in t:
        #         cr.move_to(x, y)
        #         cr.show_text(throw)

        #         ext = cr.text_extents(throw)
        #         x += ext.x_advance + 10  # spacing between throws

        #     # --- 4️⃣ move to next line ---
        #     y += 22   # or use font_extents for dynamic spacing

class ScoreAreaTop(BaseScoreArea):
    __gtype_name__ = "ScoreAreaTop"
    def __init__(self):
        super().__init__((0.95, 0.95, 1))

class ScoreAreaBottom(BaseScoreArea):
    __gtype_name__ = "ScoreAreaBottom"
    def __init__(self):
        super().__init__((0.95, 1, 0.95))
