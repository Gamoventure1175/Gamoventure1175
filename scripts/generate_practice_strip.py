#!/usr/bin/env python3
"""Generate the animated interests strip used by the profile README."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from math import pi, sin
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageSequence


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIRECTORY = ROOT / "assets" / "illustrations"
GIF_PATH = OUTPUT_DIRECTORY / "practice-strip-graphite.gif"
STILL_PATH = OUTPUT_DIRECTORY / "practice-strip-graphite-still.png"

WIDTH = 1280
HEIGHT = 260
RENDER_SCALE = 2
FRAME_COUNT = 100
FRAME_DURATION_MS = 60

BACKGROUND_TOP = "#090D13"
BACKGROUND_BOTTOM = "#0B1119"
SURFACE = "#101720"
GRID = "#17212D"
BORDER = "#2A3747"
BORDER_HIGHLIGHT = "#34475A"
FOREGROUND = "#E7EDF4"
MUTED = "#8E9BAA"
MUTED_DARK = "#657486"
ACCENT = "#62B0D5"
ACCENT_BRIGHT = "#70C5E8"
ACCENT_DARK = "#1E4A65"
CYAN = "#69C5C3"
PORTAL_BLUE = "#65B5E8"
PORTAL_BLUE_DARK = "#245675"
PORTAL_ORANGE = "#C47D52"
PORTAL_ORANGE_DARK = "#643D2E"
KEY_SURFACE = "#161F2A"
CUBE_OUTLINE = "#06090D"
SHADOW = "#05070B"

CUBE_COLORS = {
    "U": "#EDF2F5",
    "D": "#E3CB47",
    "F": "#35A36F",
    "B": "#3C73C9",
    "R": "#C94E57",
    "L": "#D17A45",
}

FONT_DIRECTORY = Path("/usr/share/fonts/truetype/dejavu")


@dataclass(frozen=True)
class Sticker:
    position: tuple[int, int, int]
    normal: tuple[int, int, int]
    color: str


CubeState = tuple[Sticker, ...]
Point = tuple[float, float]


def load_font(filename: str, size: int) -> ImageFont.FreeTypeFont:
    path = FONT_DIRECTORY / filename
    if not path.exists():
        raise RuntimeError(f"Required font is not available: {path}")
    return ImageFont.truetype(str(path), size=size * RENDER_SCALE)


LABEL_FONT = load_font("DejaVuSansMono-Bold.ttf", 12)
SMALL_FONT = load_font("DejaVuSansMono.ttf", 10)
SMALL_BOLD_FONT = load_font("DejaVuSansMono-Bold.ttf", 11)
METRIC_FONT = load_font("DejaVuSans-Bold.ttf", 34)
METRIC_COMPACT_FONT = load_font("DejaVuSans-Bold.ttf", 27)
LARGE_METRIC_FONT = load_font("DejaVuSans-Bold.ttf", 44)


class ScaledDraw:
    """Draw in logical pixels while rendering at a higher internal resolution."""

    def __init__(self, image: Image.Image) -> None:
        self._draw = ImageDraw.Draw(image)

    @staticmethod
    def _point(point: Point) -> Point:
        return point[0] * RENDER_SCALE, point[1] * RENDER_SCALE

    @classmethod
    def _coordinates(cls, coordinates):
        if coordinates and isinstance(coordinates[0], (tuple, list)):
            return [cls._point(point) for point in coordinates]
        return tuple(value * RENDER_SCALE for value in coordinates)

    def line(self, coordinates, *, fill, width: int = 1, **kwargs) -> None:
        self._draw.line(
            self._coordinates(coordinates),
            fill=fill,
            width=max(1, width * RENDER_SCALE),
            **kwargs,
        )

    def rounded_rectangle(
        self,
        coordinates,
        *,
        radius: int,
        fill=None,
        outline=None,
        width: int = 1,
    ) -> None:
        self._draw.rounded_rectangle(
            self._coordinates(coordinates),
            radius=radius * RENDER_SCALE,
            fill=fill,
            outline=outline,
            width=max(1, width * RENDER_SCALE),
        )

    def ellipse(self, coordinates, *, fill=None, outline=None, width: int = 1) -> None:
        self._draw.ellipse(
            self._coordinates(coordinates),
            fill=fill,
            outline=outline,
            width=max(1, width * RENDER_SCALE),
        )

    def polygon(self, coordinates, *, fill=None, outline=None, width: int = 1) -> None:
        self._draw.polygon(
            self._coordinates(coordinates),
            fill=fill,
            outline=outline,
            width=max(1, width * RENDER_SCALE),
        )

    def text(self, point, text, *, font, fill, **kwargs) -> None:
        self._draw.text(self._point(point), text, font=font, fill=fill, **kwargs)

    def textbbox(self, point, text, *, font, **kwargs):
        box = self._draw.textbbox(self._point(point), text, font=font, **kwargs)
        return tuple(value / RENDER_SCALE for value in box)


def solved_cube() -> CubeState:
    stickers: list[Sticker] = []
    for first in (-1, 0, 1):
        for second in (-1, 0, 1):
            stickers.extend(
                (
                    Sticker((first, 1, second), (0, 1, 0), CUBE_COLORS["U"]),
                    Sticker((first, -1, second), (0, -1, 0), CUBE_COLORS["D"]),
                    Sticker((first, second, 1), (0, 0, 1), CUBE_COLORS["F"]),
                    Sticker((first, second, -1), (0, 0, -1), CUBE_COLORS["B"]),
                    Sticker((1, first, second), (1, 0, 0), CUBE_COLORS["R"]),
                    Sticker((-1, first, second), (-1, 0, 0), CUBE_COLORS["L"]),
                )
            )
    return tuple(stickers)


def rotate_vector(
    vector: tuple[int, int, int], axis: str, direction: int
) -> tuple[int, int, int]:
    x, y, z = vector
    if axis == "x":
        return (x, -direction * z, direction * y)
    if axis == "y":
        return (direction * z, y, -direction * x)
    if axis == "z":
        return (-direction * y, direction * x, z)
    raise ValueError(f"Unsupported rotation axis: {axis}")


MOVE_DEFINITIONS = {
    "R": ("x", 1, -1),
    "L": ("x", -1, 1),
    "U": ("y", 1, 1),
    "D": ("y", -1, -1),
    "F": ("z", 1, -1),
    "B": ("z", -1, 1),
}


def apply_move(state: CubeState, move: str) -> CubeState:
    face = move[0]
    axis, layer, base_direction = MOVE_DEFINITIONS[face]
    turns = 2 if move.endswith("2") else 1
    direction = -base_direction if move.endswith("'") else base_direction

    result = state
    axis_index = {"x": 0, "y": 1, "z": 2}[axis]
    for _ in range(turns):
        rotated: list[Sticker] = []
        for sticker in result:
            if sticker.position[axis_index] != layer:
                rotated.append(sticker)
                continue
            rotated.append(
                Sticker(
                    rotate_vector(sticker.position, axis, direction),
                    rotate_vector(sticker.normal, axis, direction),
                    sticker.color,
                )
            )
        result = tuple(rotated)
    return result


def invert_move(move: str) -> str:
    if move.endswith("2"):
        return move
    if move.endswith("'"):
        return move[0]
    return f"{move}'"


def validate_cube_state(state: CubeState) -> None:
    sticker_positions = {(sticker.position, sticker.normal) for sticker in state}
    color_counts = Counter(sticker.color for sticker in state)
    if len(state) != 54 or len(sticker_positions) != 54:
        raise RuntimeError("Cube state must contain 54 uniquely positioned stickers")
    if set(color_counts) != set(CUBE_COLORS.values()):
        raise RuntimeError("Cube state contains an unsupported sticker color")
    if any(count != 9 for count in color_counts.values()):
        raise RuntimeError("Each cube color must appear on exactly nine stickers")


def build_solve_states() -> tuple[list[CubeState], list[str]]:
    scramble = ["R", "U", "F", "R'", "U2", "F'"]
    state = solved_cube()
    validate_cube_state(state)
    for move in scramble:
        state = apply_move(state, move)
        validate_cube_state(state)

    solve_moves = [invert_move(move) for move in reversed(scramble)]
    states = [state]
    for move in solve_moves:
        state = apply_move(state, move)
        validate_cube_state(state)
        states.append(state)

    if state != solved_cube():
        raise RuntimeError("The configured solve sequence does not restore the cube")
    return states, solve_moves


SOLVE_STATES, SOLVE_MOVES = build_solve_states()


def clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    return max(minimum, min(maximum, value))


def smoothstep(value: float) -> float:
    value = clamp(value)
    return value * value * (3.0 - 2.0 * value)


def color_tuple(color: str) -> tuple[int, int, int]:
    return (
        int(color[1:3], 16),
        int(color[3:5], 16),
        int(color[5:7], 16),
    )


def blend_color(first: str, second: str, amount: float) -> str:
    amount = clamp(amount)
    first_rgb = color_tuple(first)
    second_rgb = color_tuple(second)
    channels = (
        round(start + (end - start) * amount)
        for start, end in zip(first_rgb, second_rgb)
    )
    return "#" + "".join(f"{channel:02X}" for channel in channels)


def mix(first: Point, second: Point, amount: float) -> Point:
    return (
        first[0] + (second[0] - first[0]) * amount,
        first[1] + (second[1] - first[1]) * amount,
    )


def quadrilateral_point(
    top_left: Point,
    top_right: Point,
    bottom_right: Point,
    bottom_left: Point,
    horizontal: float,
    vertical: float,
) -> Point:
    top = mix(top_left, top_right, horizontal)
    bottom = mix(bottom_left, bottom_right, horizontal)
    return mix(top, bottom, vertical)


def sticker_lookup(
    state: CubeState,
) -> dict[tuple[tuple[int, int, int], tuple[int, int, int]], str]:
    return {(sticker.position, sticker.normal): sticker.color for sticker in state}


def visible_face_matrices(state: CubeState) -> tuple[list[list[str]], ...]:
    lookup = sticker_lookup(state)

    top = [
        [lookup[((x, 1, z), (0, 1, 0))] for x in (-1, 0, 1)]
        for z in (-1, 0, 1)
    ]
    front = [
        [lookup[((x, y, 1), (0, 0, 1))] for x in (-1, 0, 1)]
        for y in (1, 0, -1)
    ]
    right = [
        [lookup[((1, y, z), (1, 0, 0))] for z in (1, 0, -1)]
        for y in (1, 0, -1)
    ]
    return top, front, right


def draw_sticker_face(
    draw: ScaledDraw,
    corners: tuple[Point, Point, Point, Point],
    colors: list[list[str]],
) -> None:
    top_left, top_right, bottom_right, bottom_left = corners
    for row in range(3):
        for column in range(3):
            left = column / 3
            right = (column + 1) / 3
            top = row / 3
            bottom = (row + 1) / 3
            polygon = [
                quadrilateral_point(
                    top_left, top_right, bottom_right, bottom_left, left, top
                ),
                quadrilateral_point(
                    top_left, top_right, bottom_right, bottom_left, right, top
                ),
                quadrilateral_point(
                    top_left, top_right, bottom_right, bottom_left, right, bottom
                ),
                quadrilateral_point(
                    top_left, top_right, bottom_right, bottom_left, left, bottom
                ),
            ]
            draw.polygon(polygon, fill=colors[row][column], outline=CUBE_OUTLINE, width=1)


def shade_face(colors: list[list[str]], amount: float) -> list[list[str]]:
    target = "#FFFFFF" if amount >= 0 else SHADOW
    return [
        [blend_color(color, target, abs(amount)) for color in row]
        for row in colors
    ]


def render_cube_layer(
    state: CubeState,
    horizontal_offset: float,
    vertical_offset: float,
) -> Image.Image:
    layer = Image.new(
        "RGBA", (WIDTH * RENDER_SCALE, HEIGHT * RENDER_SCALE), (0, 0, 0, 0)
    )
    draw = ScaledDraw(layer)

    def shifted(point: Point) -> Point:
        return point[0] + horizontal_offset, point[1] + vertical_offset

    top_colors, front_colors, right_colors = visible_face_matrices(state)
    top_colors = shade_face(top_colors, 0.08)
    front_colors = shade_face(front_colors, -0.02)
    right_colors = shade_face(right_colors, -0.13)
    top = tuple(
        shifted(point)
        for point in ((116, 77), (166, 98), (117, 121), (67, 100))
    )
    front = tuple(
        shifted(point)
        for point in ((67, 100), (117, 121), (117, 181), (67, 157))
    )
    right = tuple(
        shifted(point)
        for point in ((117, 121), (166, 98), (166, 157), (117, 181))
    )

    draw_sticker_face(draw, top, top_colors)
    draw_sticker_face(draw, front, front_colors)
    draw_sticker_face(draw, right, right_colors)
    return layer


def draw_cube(
    image: Image.Image,
    draw: ScaledDraw,
    from_state: CubeState,
    to_state: CubeState,
    transition: float,
    horizontal_offset: float,
    vertical_offset: float,
    move_label: str | None,
) -> None:
    first_layer = render_cube_layer(from_state, horizontal_offset, vertical_offset)
    if from_state == to_state or transition <= 0.0:
        cube_layer = first_layer
    else:
        second_layer = render_cube_layer(to_state, horizontal_offset, vertical_offset)
        cube_layer = Image.blend(first_layer, second_layer, transition)
    image.paste(cube_layer, (0, 0), cube_layer)

    if move_label:
        chip_x = 171 + horizontal_offset
        chip_y = 77 + vertical_offset
        draw.rounded_rectangle(
            (chip_x, chip_y, chip_x + 24, chip_y + 19),
            radius=4,
            fill=ACCENT_DARK,
            outline=ACCENT,
            width=1,
        )
        draw.text(
            (chip_x + 5, chip_y + 3),
            move_label,
            font=SMALL_BOLD_FONT,
            fill=FOREGROUND,
        )


def cube_state_at(
    time_seconds: float,
) -> tuple[CubeState, CubeState, float, str | None, float, float]:
    if time_seconds < 0.6:
        return SOLVE_STATES[0], SOLVE_STATES[0], 0.0, None, 0.0, 0.0

    if time_seconds < 3.3:
        move_duration = 0.45
        phase = (time_seconds - 0.6) / move_duration
        move_index = min(int(phase), len(SOLVE_MOVES) - 1)
        within_move = phase - int(phase)
        transition = smoothstep(within_move)
        direction = -1 if move_index % 2 else 1
        motion_curve = sin(pi * within_move)
        horizontal = direction * 1.25 * motion_curve
        vertical = -1.15 * motion_curve
        return (
            SOLVE_STATES[move_index],
            SOLVE_STATES[move_index + 1],
            transition,
            SOLVE_MOVES[move_index],
            horizontal,
            vertical,
        )

    if time_seconds < 4.8:
        return SOLVE_STATES[-1], SOLVE_STATES[-1], 0.0, None, 0.0, 0.0

    if time_seconds < 5.5:
        reset_progress = smoothstep((time_seconds - 4.8) / 0.7)
        vertical = -0.75 * sin(pi * reset_progress)
        return (
            SOLVE_STATES[-1],
            SOLVE_STATES[0],
            reset_progress,
            None,
            0.0,
            vertical,
        )

    return SOLVE_STATES[0], SOLVE_STATES[0], 0.0, None, 0.0, 0.0


def draw_grid(draw: ScaledDraw) -> None:
    for x in range(64, WIDTH, 64):
        draw.line((x, 0, x, HEIGHT), fill=GRID, width=1)
    for y in range(52, HEIGHT, 52):
        draw.line((0, y, WIDTH, y), fill=GRID, width=1)


def draw_panel_header(
    draw: ScaledDraw, x: int, label: str, accent: str = ACCENT
) -> None:
    draw.rounded_rectangle(
        (x + 24, 41, x + 29, 46), radius=2, fill=accent, outline=accent
    )
    draw.text((x + 39, 36), label, font=LABEL_FONT, fill=MUTED)
    draw.line((x + 24, 62, x + 370, 62), fill=BORDER, width=1)
    draw.line((x + 24, 62, x + 80, 62), fill=accent, width=2)


def draw_cube_panel(
    image: Image.Image, draw: ScaledDraw, time_seconds: float
) -> None:
    draw_panel_header(draw, 24, "SPEEDCUBING", CYAN)
    from_state, to_state, transition, move_label, horizontal, vertical = cube_state_at(
        time_seconds
    )
    draw.ellipse((78, 174, 158, 187), fill=SHADOW)
    draw_cube(
        image,
        draw,
        from_state,
        to_state,
        transition,
        horizontal,
        vertical,
        move_label,
    )

    draw.text((198, 94), "8.76s", font=METRIC_FONT, fill=FOREGROUND)
    draw.text((342, 112), "PB", font=SMALL_BOLD_FONT, fill=CYAN)
    draw.line((198, 141, 369, 141), fill=BORDER, width=1)
    draw.line((198, 141, 284, 141), fill=CYAN, width=2)
    draw.text((198, 155), "10–15s", font=METRIC_COMPACT_FONT, fill=FOREGROUND)
    draw.text((335, 180), "TYPICAL", font=SMALL_FONT, fill=MUTED)


KEY_ROWS = (
    ("QWERTYUIOP", 467, 79),
    ("ASDFGHJKL", 484, 108),
    ("ZXCVBNM", 518, 137),
)
TYPING_SEQUENCE = "CLEAR SYSTEMS STAY SIMPLE "


def active_key_state(time_seconds: float) -> tuple[str | None, float]:
    if time_seconds < 0.25 or time_seconds >= 4.65:
        return None, 0.0
    key_position = (time_seconds - 0.25) * 10.5
    index = int(key_position)
    press_amount = sin(pi * (key_position - index))
    return TYPING_SEQUENCE[index % len(TYPING_SEQUENCE)], smoothstep(press_amount)


def typing_progress(time_seconds: float) -> float:
    if time_seconds < 0.25:
        return 0.0
    if time_seconds < 4.65:
        return smoothstep((time_seconds - 0.25) / 4.4)
    if time_seconds < 4.9:
        return 1.0
    if time_seconds < 5.5:
        return 1.0 - smoothstep((time_seconds - 4.9) / 0.6)
    return 0.0


def draw_keyboard(draw: ScaledDraw, time_seconds: float) -> None:
    pressed, press_amount = active_key_state(time_seconds)
    key_width = 28
    key_height = 22
    gap = 5

    for letters, start_x, start_y in KEY_ROWS:
        for index, letter in enumerate(letters):
            x = start_x + index * (key_width + gap)
            is_pressed = pressed == letter
            key_press = press_amount if is_pressed else 0.0
            offset = 2.0 * key_press
            fill = blend_color(KEY_SURFACE, ACCENT_DARK, key_press * 0.78)
            outline = blend_color(BORDER, ACCENT_BRIGHT, key_press)
            label_color = blend_color(MUTED, FOREGROUND, key_press)
            draw.rounded_rectangle(
                (x, start_y + 2, x + key_width, start_y + key_height + 2),
                radius=3,
                fill=SHADOW,
                outline=SHADOW,
            )
            draw.rounded_rectangle(
                (x, start_y + offset, x + key_width, start_y + key_height + offset),
                radius=3,
                fill=fill,
                outline=outline,
                width=1,
            )
            text_box = draw.textbbox((0, 0), letter, font=SMALL_FONT)
            text_width = text_box[2] - text_box[0]
            draw.text(
                (x + (key_width - text_width) / 2, start_y + 5 + offset),
                letter,
                font=SMALL_FONT,
                fill=label_color,
            )

    space_press = press_amount if pressed == " " else 0.0
    space_offset = 2.0 * space_press
    draw.rounded_rectangle(
        (567, 168, 708, 186),
        radius=3,
        fill=SHADOW,
        outline=SHADOW,
    )
    draw.rounded_rectangle(
        (567, 166 + space_offset, 708, 184 + space_offset),
        radius=3,
        fill=blend_color(KEY_SURFACE, ACCENT_DARK, space_press * 0.78),
        outline=blend_color(BORDER, ACCENT_BRIGHT, space_press),
        width=1,
    )
    draw.line(
        (593, 175 + space_offset, 682, 175 + space_offset),
        fill=blend_color(MUTED_DARK, ACCENT_BRIGHT, space_press),
        width=2,
    )

    draw.line((674, 204, 793, 204), fill=BORDER, width=1)
    progress = typing_progress(time_seconds)
    if progress > 0.0:
        draw.line((674, 204, 674 + 119 * progress, 204), fill=ACCENT, width=2)


def draw_typing_panel(draw: ScaledDraw, time_seconds: float) -> None:
    draw_panel_header(draw, 443, "TYPING", ACCENT)
    draw_keyboard(draw, time_seconds)
    draw.text((477, 192), "90+", font=LARGE_METRIC_FONT, fill=FOREGROUND)
    draw.text((583, 210), "WPM", font=SMALL_BOLD_FONT, fill=ACCENT)


def opening_progress(time_seconds: float, start: float, end: float) -> float:
    if time_seconds < start:
        return 0.0
    if time_seconds < end:
        return smoothstep((time_seconds - start) / (end - start))
    if time_seconds < 4.9:
        return 1.0
    if time_seconds < 5.5:
        return 1.0 - smoothstep((time_seconds - 4.9) / 0.6)
    return 0.0


def draw_portal(
    image: Image.Image,
    draw: ScaledDraw,
    center: tuple[int, int],
    color: str,
    dark_color: str,
    progress: float,
) -> None:
    if progress <= 0.01:
        return
    center_x, center_y = center
    radius_x = 3 + 7 * progress
    radius_y = 4 + 31 * progress

    glow = Image.new(
        "RGBA", (WIDTH * RENDER_SCALE, HEIGHT * RENDER_SCALE), (0, 0, 0, 0)
    )
    glow_draw = ScaledDraw(glow)
    glow_draw.ellipse(
        (
            center_x - radius_x - 3,
            center_y - radius_y - 3,
            center_x + radius_x + 3,
            center_y + radius_y + 3,
        ),
        outline=(*color_tuple(color), round(90 * progress)),
        width=5,
    )
    glow = glow.filter(ImageFilter.GaussianBlur(5 * RENDER_SCALE))
    image.paste(glow, (0, 0), glow)

    draw.ellipse(
        (
            center_x - radius_x - 3,
            center_y - radius_y - 3,
            center_x + radius_x + 3,
            center_y + radius_y + 3,
        ),
        outline=dark_color,
        width=2,
    )
    draw.ellipse(
        (
            center_x - radius_x,
            center_y - radius_y,
            center_x + radius_x,
            center_y + radius_y,
        ),
        fill=blend_color(SURFACE, SHADOW, 0.58),
        outline=color,
        width=2,
    )
    inner_x = max(1.5, radius_x - 4)
    inner_y = max(2, radius_y - 8)
    draw.ellipse(
        (
            center_x - inner_x,
            center_y - inner_y,
            center_x + inner_x,
            center_y + inner_y,
        ),
        outline=blend_color(color, FOREGROUND, 0.28),
        width=1,
    )


def bezier_points(
    start: Point, control_one: Point, control_two: Point, end: Point, steps: int
) -> list[Point]:
    points = []
    for index in range(steps + 1):
        amount = index / steps
        inverse = 1.0 - amount
        x = (
            inverse**3 * start[0]
            + 3 * inverse**2 * amount * control_one[0]
            + 3 * inverse * amount**2 * control_two[0]
            + amount**3 * end[0]
        )
        y = (
            inverse**3 * start[1]
            + 3 * inverse**2 * amount * control_one[1]
            + 3 * inverse * amount**2 * control_two[1]
            + amount**3 * end[1]
        )
        points.append((x, y))
    return points


def draw_portal_panel(
    image: Image.Image, draw: ScaledDraw, time_seconds: float
) -> None:
    draw_panel_header(draw, 862, "FAVOURITE GAME", PORTAL_BLUE)

    draw.line((886, 176, 1232, 176), fill=BORDER, width=1)
    draw.line((930, 172, 930, 180), fill=MUTED_DARK, width=1)
    draw.line((1188, 172, 1188, 180), fill=MUTED_DARK, width=1)

    blue_progress = opening_progress(time_seconds, 0.35, 1.0)
    orange_progress = opening_progress(time_seconds, 1.15, 1.8)
    draw_portal(
        image, draw, (930, 136), PORTAL_BLUE, PORTAL_BLUE_DARK, blue_progress
    )
    draw_portal(
        image, draw, (1188, 128), PORTAL_ORANGE, PORTAL_ORANGE_DARK, orange_progress
    )

    if orange_progress > 0.78:
        route = bezier_points((941, 136), (1000, 76), (1121, 83), (1177, 128), 48)
        draw.line(route, fill=MUTED_DARK, width=1)
        if 2.0 <= time_seconds < 4.5:
            travel = smoothstep((time_seconds - 2.0) / 2.5)
            highlight_end = min(
                int(travel * (len(route) - 1)) + 1, len(route) - 1
            )
            highlight_start = max(0, highlight_end - 7)
            draw.line(
                route[highlight_start : highlight_end + 1],
                fill=ACCENT_BRIGHT,
                width=2,
            )

    draw.text((886, 192), "PORTAL", font=METRIC_FONT, fill=FOREGROUND)
    draw.text((1048, 210), "PLAY / REPLAY", font=SMALL_FONT, fill=MUTED)
    draw.line((1184, 207, 1232, 207), fill=BORDER, width=1)
    draw.line((1184, 207, 1208, 207), fill=PORTAL_BLUE, width=2)


def render_static_base() -> Image.Image:
    image = Image.new(
        "RGB", (WIDTH * RENDER_SCALE, HEIGHT * RENDER_SCALE), BACKGROUND_TOP
    )
    raw_draw = ImageDraw.Draw(image)
    for y in range(HEIGHT * RENDER_SCALE):
        amount = y / max(1, HEIGHT * RENDER_SCALE - 1)
        raw_draw.line(
            (0, y, WIDTH * RENDER_SCALE, y),
            fill=blend_color(BACKGROUND_TOP, BACKGROUND_BOTTOM, amount),
        )

    draw = ScaledDraw(image)
    draw_grid(draw)

    shadow_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    shadow_draw = ScaledDraw(shadow_layer)
    for left in (24, 443, 862):
        shadow_draw.rounded_rectangle(
            (left, 29, left + 394, 241),
            radius=12,
            fill=(2, 5, 9, 145),
        )
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(7 * RENDER_SCALE))
    image.paste(shadow_layer, (0, 0), shadow_layer)

    draw = ScaledDraw(image)
    for left in (24, 443, 862):
        draw.rounded_rectangle(
            (left, 24, left + 394, 236),
            radius=12,
            fill=SURFACE,
            outline=BORDER,
            width=1,
        )
        draw.line(
            (left + 14, 25, left + 380, 25),
            fill=BORDER_HIGHLIGHT,
            width=1,
        )
    return image


def render_frame(time_seconds: float, static_base: Image.Image) -> Image.Image:
    image = static_base.copy()
    draw = ScaledDraw(image)

    draw_cube_panel(image, draw, time_seconds)
    draw_typing_panel(draw, time_seconds)
    draw_portal_panel(image, draw, time_seconds)
    return image.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS).convert("RGB")


def save_gif(frames: list[Image.Image]) -> None:
    palette_samples = frames[::10]
    palette_source = Image.new("RGB", (WIDTH, HEIGHT * len(palette_samples)))
    for index, frame in enumerate(palette_samples):
        palette_source.paste(frame, (0, index * HEIGHT))
    palette = palette_source.quantize(
        colors=128,
        method=Image.Quantize.MEDIANCUT,
        dither=Image.Dither.NONE,
    )
    indexed_frames = [
        frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames
    ]
    indexed_frames[0].save(
        GIF_PATH,
        save_all=True,
        append_images=indexed_frames[1:],
        duration=FRAME_DURATION_MS,
        loop=0,
        optimize=True,
        disposal=1,
    )


def verify_outputs() -> None:
    with Image.open(GIF_PATH) as animation:
        durations = [
            frame.info.get("duration", 0) for frame in ImageSequence.Iterator(animation)
        ]
        if animation.size != (WIDTH, HEIGHT):
            raise RuntimeError(f"Unexpected GIF dimensions: {animation.size}")
        if not animation.is_animated or animation.n_frames < 75:
            raise RuntimeError("The generated GIF does not contain the expected motion")
        if animation.info.get("loop") != 0:
            raise RuntimeError("The generated GIF is not configured to loop")
        if sum(durations) != FRAME_COUNT * FRAME_DURATION_MS:
            raise RuntimeError("The generated GIF has an unexpected cycle duration")

    with Image.open(STILL_PATH) as still:
        if still.size != (WIDTH, HEIGHT):
            raise RuntimeError(f"Unexpected still-image dimensions: {still.size}")

    if GIF_PATH.stat().st_size > 1_000_000:
        raise RuntimeError("The generated GIF exceeds the one-megabyte asset budget")


def main() -> None:
    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    static_base = render_static_base()
    frames = [
        render_frame(index * FRAME_DURATION_MS / 1000, static_base)
        for index in range(FRAME_COUNT)
    ]
    save_gif(frames)
    render_frame(4.2, static_base).save(STILL_PATH, optimize=True)
    verify_outputs()
    print(f"generated {GIF_PATH.relative_to(ROOT)} ({FRAME_COUNT} frames)")
    print(f"generated {STILL_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
