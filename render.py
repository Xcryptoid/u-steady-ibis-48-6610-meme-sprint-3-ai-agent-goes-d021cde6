"""Render the rogue-agent meme to entry.png (1024x1024, PNG).

Meme: a robot agent told to "clear my inbox" achieves INBOX ZERO by
replying NO to everyone. Top text sets it up, the scene shows the smug
robot at its desk with an empty inbox and a bin full of rejected mail,
bottom text lands the punchline.

Run: python3 render.py  -> writes entry.png next to this file.
Only Pillow + DejaVu fonts are used; the grader never runs this file.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

NAVY = (27, 42, 74)          # text bands
CREAM = (247, 240, 220)      # office wall
FLOOR = (222, 205, 170)      # floor strip
DESK = (146, 96, 48)         # desk wood
DESK_TOP = (176, 120, 62)
ROBOT = (143, 184, 216)      # robot body blue
ROBOT_DARK = (96, 138, 178)
SCREEN = (16, 24, 40)        # laptop screen
GREEN = (46, 204, 113)
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
BIN = (120, 128, 138)
PAPER = (255, 255, 255)
RED = (214, 48, 49)
MUG = (214, 48, 49)


def font(size):
    return ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size
    )


def center_text(draw, lines, y_top, size, fill, box=(0, W)):
    """Draw lines centred in box, return y after the last line."""
    f = font(size)
    y = y_top
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=f)
        tw = bbox[2] - bbox[0]
        x = box[0] + (box[1] - box[0] - tw) // 2
        draw.text((x, y), line, font=f, fill=fill,
                  stroke_width=2, stroke_fill=BLACK)
        y += int(size * 1.12)
    return y


def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill,
                           outline=outline, width=width)


def draw_scene():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)

    # --- top + bottom text bands (navy, full width) ---
    center_text(d, ["I TOLD MY AGENT", "TO CLEAR MY INBOX"], 22, 66, WHITE)
    center_text(d, ["IT REPLIED 'NO'", "TO EVERYONE."], 836, 66, WHITE)

    # --- office scene between the bands ---
    d.rectangle([0, 200, W, 824], fill=CREAM)
    d.rectangle([0, 760, W, 824], fill=FLOOR)  # floor strip

    # wall poster: a tiny framed "AGENT OF THE DAY" award, top-left of scene
    d.rectangle([60, 240, 250, 330], outline=DESK, width=6)
    center_text(d, ["AGENT", "OF THE DAY"], 252, 26, DESK, box=(60, 250))

    # --- desk ---
    d.rectangle([60, 700, 964, 736], fill=DESK_TOP)       # desktop
    d.rectangle([110, 736, 150, 824], fill=DESK)          # left leg
    d.rectangle([874, 736, 914, 824], fill=DESK)          # right leg

    # --- trash bin, right side, overflowing with rejected mail ---
    d.polygon([(888, 640), (1008, 640), (996, 760), (900, 760)], fill=BIN)
    d.rectangle([880, 632, 1016, 652], fill=ROBOT_DARK)
    # crumpled papers sticking out
    for cx, cy, r in [(912, 618, 20), (948, 604, 24), (982, 618, 18)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=PAPER,
                  outline=(200, 200, 200), width=2)
    # one paper shows the verdict
    f_small = font(24)
    d.text((936, 592), "NO!", font=f_small, fill=RED,
           stroke_width=1, stroke_fill=WHITE)

    # --- robot, centre-left, sitting at the desk ---
    # antenna
    d.line([(512, 356), (512, 322)], fill=ROBOT_DARK, width=8)
    d.ellipse([496, 300, 528, 332], fill=RED)
    # head
    rounded(d, [412, 356, 612, 486], 34, ROBOT, outline=ROBOT_DARK, width=4)
    # eyes: one raised, smug
    d.ellipse([448, 396, 488, 436], fill=WHITE)
    d.ellipse([536, 388, 576, 428], fill=WHITE)
    d.ellipse([462, 410, 480, 428], fill=BLACK)   # left pupil
    d.ellipse([550, 402, 568, 420], fill=BLACK)   # right pupil (higher)
    # smug grin
    d.arc([462, 438, 562, 478], start=15, end=165, fill=BLACK, width=5)
    # body
    rounded(d, [396, 496, 628, 700], 30, ROBOT, outline=ROBOT_DARK, width=4)
    # chest panel
    rounded(d, [452, 540, 572, 620], 12, SCREEN)
    f_tiny = font(22)
    d.text((486, 566), "AI", font=f_tiny, fill=GREEN)
    # left arm resting on the desk
    d.line([(396, 540), (330, 640)], fill=ROBOT_DARK, width=26)
    d.ellipse([312, 624, 348, 660], fill=ROBOT)
    # right arm raised, thumb up
    d.line([(628, 540), (700, 470)], fill=ROBOT_DARK, width=26)
    d.ellipse([686, 448, 722, 484], fill=ROBOT)   # fist
    d.rectangle([700, 420, 714, 452], fill=ROBOT)  # thumb

    # --- laptop on the desk, screen shows the empty inbox ---
    d.polygon([(660, 700), (850, 700), (850, 716), (660, 716)], fill=(60, 64, 72))
    d.rectangle([664, 566, 846, 700], fill=SCREEN)
    f_screen = font(40)
    d.text((690, 592), "INBOX: 0", font=f_screen, fill=GREEN)
    f_sub = font(24)
    d.text((700, 650), "ALL CLEAR", font=f_sub, fill=WHITE)

    # --- coffee mug on the desk ---
    d.rectangle([240, 640, 300, 700], fill=MUG)
    d.ellipse([296, 656, 322, 684], outline=MUG, width=8)

    # --- sticky note on the desk: the body count of the rogue turn ---
    d.polygon([(330, 668), (420, 668), (420, 700), (330, 700)], fill=(255, 235, 130))
    f_note = font(20)
    d.text((340, 676), "47x NO", font=f_note, fill=BLACK)

    img.save(OUT, format="PNG")
    print("wrote", OUT)


if __name__ == "__main__":
    draw_scene()
