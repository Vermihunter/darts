import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GObject
import math

# ---- Normalized radii ----
INNER_BULL = 6.35 / 170
OUTER_BULL = 15.9 / 170
TRIPLE_INNER = 99.0 / 170
TRIPLE_OUTER = 107.0 / 170
DOUBLE_INNER = 162.0 / 170
BOARD_EDGE = 1.0

# ---- Colors ----
GREEN = (0.0, 0.45, 0.0)
RED = (0.75, 0.0, 0.0)
BLACK = (0.07, 0.07, 0.07)
CREAM = (0.95, 0.90, 0.75)
BOARD_BG = (0.1, 0.1, 0.1)

# 20-segment clockwise numbering
NUMBERS = [20, 1, 18, 4, 13, 6, 10, 15, 2, 17,
           3, 19, 7, 16, 8, 11, 14, 9, 12, 5]


@Gtk.Template(resource_path="/com/vermesa/darts/ui/darts_board.ui")
class DartsBoard(Gtk.Box):
    __gtype_name__ = "DartsBoard"
    
    __gsignals__ = {
        # name        arg types tuple           return type
        "throw": (GObject.SignalFlags.RUN_FIRST, None,
                  (str, int, int))  # ring, base, score
    }

    canvas = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # connect draw function
        self.canvas.set_draw_func(self.on_draw)
        
        self.click = Gtk.GestureClick()
        self.click.connect("pressed", self.on_click)
        self.canvas.add_controller(self.click)
        
    def on_click(self, gesture, n_press, x, y):
        # center + scale must match on_draw
        width  = self.canvas.get_width()
        height = self.canvas.get_height()
        cx = width / 2
        cy = height / 2
        max_r = min(width, height) * 0.44

        dx = x - cx
        dy = y - cy

        r = math.hypot(dx, dy)
        rn = r / max_r          # normalized radius 0..1

        # ---------- WHICH RING ----------
        ring = None
        score = None

        if rn <= INNER_BULL:
            ring = "INNER BULL"
            score = 50
        elif rn <= OUTER_BULL:
            ring = "OUTER BULL"
            score = 25
        elif rn <= TRIPLE_INNER:
            ring = "INNER SINGLE"
        elif rn <= TRIPLE_OUTER:
            ring = "TRIPLE"
        elif rn <= DOUBLE_INNER:
            ring = "OUTER SINGLE"
        elif rn <= BOARD_EDGE:
            ring = "DOUBLE"
        else:
            self.emit("throw", "MISS", 0, 0)
            return

        # ---------- WHICH SEGMENT ----------
        # y axis in GTK increases downward,
        # so invert dy to make 0 degrees point right,
        # then rotate so 20 is at top.
        ang = math.atan2(-dy, dx)

        # put 20 at -pi/2
        ang -= math.pi / 2

        # normalize to 0..2*pi
        ang %= 2 * math.pi

        dtheta = 2 * math.pi / 20
        idx = int(ang // dtheta)
        base = NUMBERS[-idx-1]

        # ---------- FINAL SCORE ----------
        if score is None:
            if ring == "DOUBLE":
                score = 2 * base
            elif ring == "TRIPLE":
                score = 3 * base
            else:
                score = base

        #print(f"Click at ({x:.1f},{y:.1f})  -> IDX={idx} RING={ring} BASE={base}   SCORE={score}")
        self.emit("throw", ring, base, score)



    def set_color(self, cr, rgb):
        cr.set_source_rgb(*rgb)

    def draw_ring_sector(self, cr, cx, cy, r_in, r_out, ang1, ang2):
        cr.new_sub_path()
        cr.arc(cx, cy, r_out, ang1, ang2)
        cr.arc_negative(cx, cy, r_in, ang2, ang1)
        cr.close_path()
        cr.fill()
        
    def draw_numbers(self, cr, cx, cy, max_r):
        # Same order we already use
        numbers = [20, 1, 18, 4, 13, 6, 10, 15, 2, 17,
                   3, 19, 7, 16, 8, 11, 14, 9, 12, 5]

        dtheta = 2 * math.pi / 20
        start = -math.pi / 2  # 20 at top

        # Number ring radius (just outside doubles)
        r = max_r * 1.07

        cr.select_font_face("Sans", 0, 0)
        cr.set_font_size(max_r * 0.09)  # scales with board size
        cr.set_source_rgb(1, 1, 1)      # white text

        for i, n in enumerate(numbers):
            mid = start + (i + 0.5) * dtheta

            x = cx + r * math.cos(mid)
            y = cy + r * math.sin(mid)

            # center the text
            te = cr.text_extents(str(n))
            cr.move_to(x - te.width / 2 - te.x_bearing,
                       y - te.height / 2 - te.y_bearing)
            cr.show_text(str(n))
            cr.stroke()


    def on_draw(self, area, cr, width, height):
        cx = width / 2
        cy = height / 2
        max_r = min(width, height) * 0.44

        # background
        self.set_color(cr, BOARD_BG)
        cr.paint()

        dtheta = 2 * math.pi / 20
        start = -math.pi / 2   # 20 on top

        # ---- Singles ----
        for i in range(20):
            ang1 = start + i * dtheta
            ang2 = ang1 + dtheta
            color = BLACK if i % 2 == 0 else CREAM
            self.set_color(cr, color)

            # inner single
            self.draw_ring_sector(
                cr, cx, cy,
                OUTER_BULL * max_r,
                TRIPLE_INNER * max_r,
                ang1, ang2
            )

            # outer single
            self.draw_ring_sector(
                cr, cx, cy,
                TRIPLE_OUTER * max_r,
                DOUBLE_INNER * max_r,
                ang1, ang2
            )

        # ---- Triple ring ----
        for i in range(20):
            ang1 = start + i * dtheta
            ang2 = ang1 + dtheta
            self.set_color(cr, RED if i % 2 == 0 else GREEN)
            self.draw_ring_sector(
                cr, cx, cy,
                TRIPLE_INNER * max_r,
                TRIPLE_OUTER * max_r,
                ang1, ang2
            )

        # ---- Double ring ----
        for i in range(20):
            ang1 = start + i * dtheta
            ang2 = ang1 + dtheta
            self.set_color(cr, RED if i % 2 == 0 else GREEN)
            self.draw_ring_sector(
                cr, cx, cy,
                DOUBLE_INNER * max_r,
                BOARD_EDGE * max_r,
                ang1, ang2
            )

        # ---- Bulls ----
        self.set_color(cr, GREEN)
        cr.arc(cx, cy, OUTER_BULL * max_r, 0, math.tau)
        cr.fill()

        self.set_color(cr, RED)
        cr.arc(cx, cy, INNER_BULL * max_r, 0, math.tau)
        cr.fill()

        # ---- Fine ring outlines ----
        cr.set_source_rgb(0, 0, 0)
        cr.set_line_width(1.5)
        for r in [
            INNER_BULL, OUTER_BULL,
            TRIPLE_INNER, TRIPLE_OUTER,
            DOUBLE_INNER, BOARD_EDGE
        ]:
            cr.new_sub_path()
            cr.arc(cx, cy, r * max_r, 0, math.tau)
            cr.stroke()

        self.draw_numbers(cr, cx, cy, max_r)

