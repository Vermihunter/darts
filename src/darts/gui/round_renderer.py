import math
import cairo

class RoundRenderer:
    def __init__(
        self,
        round_number,
        throws,
        font_size=15,
        spacing=10,
        padding_x=14,
        padding_y=12,
    ):
        self.round_number = round_number
        self.throws = throws
        self.font_size = font_size
        self.spacing = spacing
        self.padding_x = padding_x
        self.padding_y = padding_y

    # ---- helpers ----
    def chip_width(self, cr, text):
        ext = cr.text_extents(text)
        return ext.x_advance + 20

    def color_for_throw(self, t):
        t = t.upper()

        if t.startswith("T"):
            return (0.95, 0.30, 0.30)   # red
        if t.startswith("D"):
            return (0.25, 0.75, 0.35)   # green
        if t in ("BULL", "BULLSEYE"):
            return (0.10, 0.60, 0.90)   # blue
        return (0.80, 0.80, 0.80)       # grey

    def rounded_rect(self, cr, x, y, w, h, r):
        cr.new_sub_path()
        cr.arc(x + w - r, y + r, r, -math.pi / 2, 0)
        cr.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
        cr.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
        cr.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
        cr.close_path()

    # ---- layout ----
    def layout(self, cr):
        cr.set_font_size(self.font_size)

        prefix = f"ROUND {self.round_number}"

        pext = cr.text_extents(prefix)
        fe = cr.font_extents()

        header_h = fe[2] + 4
        chip_h = 24

        width = 71 + self.padding_x * 2 # pext.x_advance +
        width += 20  # arrow + spacing

        chip_width = 30
        for t in self.throws:
            # self.chip_width(cr, t)
            width += chip_width + self.spacing
            
        height = (
            self.padding_y * 2
            + header_h
            + 6
            + chip_h
        )

        return width, height

    # ---- drawing ----
    def draw(self, cr, x, y):
        w, h = self.layout(cr)
        radius = 12
        chip_h = 24
        
        #print(f"Width: {w}")

        # ===== SHADOW =====
        cr.save()
        cr.set_source_rgba(0, 0, 0, 0.25)
        self.rounded_rect(cr, x + 2, y + 3, w, h, radius)
        cr.fill()
        cr.restore()

        # ===== CARD BACKGROUND =====
        pat = cairo.LinearGradient(x, y, x, y + h)
        pat.add_color_stop_rgb(0, 0.16, 0.17, 0.21)
        pat.add_color_stop_rgb(1, 0.20, 0.21, 0.25)
        cr.set_source(pat)

        self.rounded_rect(cr, x, y, w, h, radius)
        cr.fill_preserve()

        cr.set_source_rgba(1, 1, 1, 0.15)
        cr.set_line_width(1.2)
        cr.stroke()

        # ===== HEADER TEXT =====
        cr.set_source_rgb(1, 1, 1)
        cr.set_font_size(self.font_size)
        cr.select_font_face(
            "Sans",
            cairo.FONT_SLANT_NORMAL,
            cairo.FONT_WEIGHT_BOLD,
        )

        prefix = f"ROUND {self.round_number}"
        hx = x + self.padding_x
        hy = y + self.padding_y + 18

        cr.move_to(hx, hy)
        cr.show_text(prefix)

        ext = cr.text_extents(prefix)
        cr.move_to(hx + ext.x_advance + 10, hy)
        #cr.show_text("→")

        # ===== CHIPS =====
        tx = x + self.padding_x
        ty = hy + 25  # consistent baseline across cards

        for t in self.throws:
            chip_w = self.chip_width(cr, t)

            # chip bg
            self.rounded_rect(cr, tx, ty - chip_h + 8, chip_w, chip_h, 11)
            cr.set_source_rgba(*self.color_for_throw(t), 0.9)
            cr.fill()

            # chip text
            cr.set_source_rgb(0, 0, 0)
            cr.set_font_size(self.font_size)
            te = cr.text_extents(t)
            text_x = tx + (chip_w - te.x_advance) / 2
            text_y = ty + 2
            cr.move_to(text_x, text_y)
            cr.show_text(t)

            tx += chip_w + self.spacing
