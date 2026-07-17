#!/usr/bin/env python3
"""Generate the animated interests strip used by the profile README."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont, ImageSequence


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIRECTORY = ROOT / "assets" / "illustrations"
GIF_PATH = OUTPUT_DIRECTORY / "practice-strip-espresso.gif"
STILL_PATH = OUTPUT_DIRECTORY / "practice-strip-still.png"

WIDTH = 1280
HEIGHT = 260
FRAME_COUNT = 75
FRAME_DURATION_MS = 80

BACKGROUND = "#181310"
SURFACE = "#221A16"
GRID = "#2B231E"
BORDER = "#4A3A31"
FOREGROUND = "#EADFD2"
MUTED = "#A49484"
CARAMEL = "#BB8464"
CARAMEL_DARK = "#684536"
CREMA = "#D7A58D"
SAGE = "#7D877E"
PORTAL_BLUE = "#6F9AA8"
PORTAL_BLUE_DARK = "#355A64"
PORTAL_ORANGE = "#CB8244"
PORTAL_ORANGE_DARK = "#754427"
KEY_SURFACE = "#2D241F"
CUBE_OUTLINE = "#100D0B"

CUBE_COLORS = {
    "U": "#F5F5F0",
    "D": "#FFD500",
    "F": "#009E60",
    "B": "#0051BA",
    "R": "#C41E3A",
    "L": "#FF6D00",
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
    return ImageFont.truetype(str(path), size=size)


LABEL_FONT = load_font("DejaVuSansMono-Bold.ttf", 12)
SMALL_FONT = load_font("DejaVuSansMono.ttf", 10)
SMALL_BOLD_FONT = load_font("DejaVuSansMono-Bold.ttf", 11)
METRIC_FONT = load_font("DejaVuSansMono-Bold.ttf", 34)
METRIC_COMPACT_FONT = load_font("DejaVuSansMono-Bold.ttf", 27)
LARGE_METRIC_FONT = load_font("DejaVuSansMono-Bold.ttf", 44)


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
    draw: ImageDraw.ImageDraw,
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
            draw.polygon(polygon, fill=colors[row][column], outline=CUBE_OUTLINE, width=2)


def draw_cube(
    draw: ImageDraw.ImageDraw,
    state: CubeState,
    horizontal_offset: float,
    vertical_offset: float,
    move_label: str | None,
) -> None:
    def shifted(point: Point) -> Point:
        return point[0] + horizontal_offset, point[1] + vertical_offset

    top_colors, front_colors, right_colors = visible_face_matrices(state)
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

    if move_label:
        draw.arc(
            (
                70 + horizontal_offset,
                72 + vertical_offset,
                165 + horizontal_offset,
                187 + vertical_offset,
            ),
            start=205,
            end=325,
            fill=CARAMEL,
            width=2,
        )
        draw.text(
            (171 + horizontal_offset, 79 + vertical_offset),
            move_label,
            font=SMALL_BOLD_FONT,
            fill=CARAMEL,
        )


def cube_state_at(time_seconds: float) -> tuple[CubeState, str | None, float, float]:
    if time_seconds < 0.6:
        return SOLVE_STATES[0], None, 0.0, 0.0

    if time_seconds < 3.3:
        move_duration = 0.45
        phase = (time_seconds - 0.6) / move_duration
        move_index = min(int(phase), len(SOLVE_MOVES) - 1)
        within_move = phase - int(phase)
        completed = move_index + (1 if within_move >= 0.62 else 0)
        state = SOLVE_STATES[min(completed, len(SOLVE_STATES) - 1)]
        direction = -1 if move_index % 2 else 1
        motion = direction * 2.4 * (1.0 - abs(within_move * 2.0 - 1.0))
        vertical = -1.8 * (1.0 - abs(within_move * 2.0 - 1.0))
        return state, SOLVE_MOVES[move_index], motion, vertical

    if time_seconds < 4.8:
        return SOLVE_STATES[-1], None, 0.0, 0.0

    if time_seconds < 5.6:
        reset_progress = clamp((time_seconds - 4.8) / 0.8)
        state_index = max(0, len(SOLVE_STATES) - 1 - int(reset_progress * len(SOLVE_MOVES)))
        return SOLVE_STATES[state_index], None, -1.5 * reset_progress, 0.0

    return SOLVE_STATES[0], None, 0.0, 0.0


def draw_grid(draw: ImageDraw.ImageDraw) -> None:
    for x in range(16, WIDTH, 32):
        draw.line((x, 0, x, HEIGHT), fill=GRID, width=1)
    for y in range(20, HEIGHT, 32):
        draw.line((0, y, WIDTH, y), fill=GRID, width=1)


def draw_panel_header(
    draw: ImageDraw.ImageDraw, x: int, label: str, portal_pair: bool = False
) -> None:
    draw.text((x + 24, 39), label, font=LABEL_FONT, fill=MUTED)
    draw.line((x + 24, 62, x + 370, 62), fill=BORDER, width=1)
    if portal_pair:
        draw.line((x + 24, 62, x + 51, 62), fill=PORTAL_BLUE, width=3)
        draw.line((x + 51, 62, x + 78, 62), fill=PORTAL_ORANGE, width=3)
        return
    draw.line((x + 24, 62, x + 51, 62), fill=SAGE, width=3)
    draw.line((x + 51, 62, x + 78, 62), fill=CARAMEL, width=3)


def draw_cube_panel(draw: ImageDraw.ImageDraw, time_seconds: float) -> None:
    draw_panel_header(draw, 24, "01 / SPEEDCUBING")
    state, move_label, horizontal, vertical = cube_state_at(time_seconds)
    draw_cube(draw, state, horizontal, vertical, move_label)

    draw.text((198, 94), "8.76s", font=METRIC_FONT, fill=FOREGROUND)
    draw.text((342, 112), "PB", font=SMALL_BOLD_FONT, fill=CARAMEL)
    draw.line((198, 141, 369, 141), fill=SAGE, width=2)
    draw.line((284, 141, 369, 141), fill=CARAMEL, width=2)
    draw.text((198, 155), "10–15s", font=METRIC_COMPACT_FONT, fill=FOREGROUND)
    draw.text((335, 180), "TYPICAL", font=SMALL_FONT, fill=MUTED)


KEY_ROWS = (
    ("QWERTYUIOP", 467, 79),
    ("ASDFGHJKL", 484, 108),
    ("ZXCVBNM", 518, 137),
)
TYPING_SEQUENCE = "CLEAR SYSTEMS STAY SIMPLE "


def active_key(time_seconds: float) -> str | None:
    if time_seconds < 0.25 or time_seconds >= 4.65:
        return None
    index = int((time_seconds - 0.25) * 10.5)
    return TYPING_SEQUENCE[index % len(TYPING_SEQUENCE)]


def draw_keyboard(draw: ImageDraw.ImageDraw, time_seconds: float) -> None:
    pressed = active_key(time_seconds)
    key_width = 28
    key_height = 22
    gap = 5

    for letters, start_x, start_y in KEY_ROWS:
        for index, letter in enumerate(letters):
            x = start_x + index * (key_width + gap)
            is_pressed = pressed == letter
            offset = 2 if is_pressed else 0
            fill = CARAMEL_DARK if is_pressed else KEY_SURFACE
            outline = CARAMEL if is_pressed else BORDER
            label_color = FOREGROUND if is_pressed else MUTED
            draw.rectangle(
                (x, start_y + offset, x + key_width, start_y + key_height + offset),
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

    space_pressed = pressed == " "
    space_offset = 2 if space_pressed else 0
    draw.rectangle(
        (567, 166 + space_offset, 708, 184 + space_offset),
        fill=CARAMEL_DARK if space_pressed else KEY_SURFACE,
        outline=CARAMEL if space_pressed else BORDER,
        width=1,
    )
    draw.line(
        (593, 175 + space_offset, 682, 175 + space_offset),
        fill=CREMA if space_pressed else SAGE,
        width=2,
    )

    if pressed is not None:
        pulse = int((time_seconds * 10.5) % 1 * 119)
        draw.line((674, 204, 674 + pulse, 204), fill=SAGE, width=2)
    draw.line((674, 204, 793, 204), fill=BORDER, width=1)


def draw_typing_panel(draw: ImageDraw.ImageDraw, time_seconds: float) -> None:
    draw_panel_header(draw, 443, "02 / TYPING")
    draw_keyboard(draw, time_seconds)
    draw.text((477, 192), "90+", font=LARGE_METRIC_FONT, fill=FOREGROUND)
    draw.text((583, 210), "WPM", font=SMALL_BOLD_FONT, fill=CARAMEL)


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
    draw: ImageDraw.ImageDraw,
    center: tuple[int, int],
    color: str,
    dark_color: str,
    progress: float,
) -> None:
    if progress <= 0.01:
        return
    center_x, center_y = center
    radius_x = 4 + 5 * progress
    radius_y = 3 + 30 * progress
    draw.ellipse(
        (
            center_x - radius_x - 4,
            center_y - radius_y - 4,
            center_x + radius_x + 4,
            center_y + radius_y + 4,
        ),
        outline=dark_color,
        width=3,
    )
    draw.ellipse(
        (
            center_x - radius_x,
            center_y - radius_y,
            center_x + radius_x,
            center_y + radius_y,
        ),
        outline=color,
        width=4,
    )
    inner_x = max(2, radius_x - 4)
    inner_y = max(2, radius_y - 8)
    draw.ellipse(
        (
            center_x - inner_x,
            center_y - inner_y,
            center_x + inner_x,
            center_y + inner_y,
        ),
        outline=color,
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


def draw_dashed_path(draw: ImageDraw.ImageDraw, points: Iterable[Point]) -> None:
    points = list(points)
    for index in range(len(points) - 1):
        if index % 4 < 2:
            draw.line((points[index], points[index + 1]), fill=MUTED, width=1)


def draw_portal_panel(draw: ImageDraw.ImageDraw, time_seconds: float) -> None:
    draw_panel_header(draw, 862, "03 / FAVOURITE GAME", portal_pair=True)

    for x in range(886, 1233, 30):
        draw.line((x, 79, x, 176), fill=GRID, width=1)
    for y in range(86, 177, 30):
        draw.line((886, y, 1232, y), fill=GRID, width=1)
    draw.line((886, 176, 1232, 176), fill=BORDER, width=1)

    blue_progress = opening_progress(time_seconds, 0.35, 1.0)
    orange_progress = opening_progress(time_seconds, 1.15, 1.8)
    draw_portal(
        draw, (930, 136), PORTAL_BLUE, PORTAL_BLUE_DARK, blue_progress
    )
    draw_portal(
        draw, (1188, 128), PORTAL_ORANGE, PORTAL_ORANGE_DARK, orange_progress
    )

    if orange_progress > 0.78:
        route = bezier_points((941, 136), (1000, 76), (1121, 83), (1177, 128), 48)
        draw_dashed_path(draw, route)
        if 2.0 <= time_seconds < 4.5:
            travel = (time_seconds - 2.0) / 2.5
            point = route[min(int(travel * (len(route) - 1)), len(route) - 1)]
            draw.ellipse(
                (point[0] - 3, point[1] - 3, point[0] + 3, point[1] + 3),
                fill=FOREGROUND,
            )

    if blue_progress > 0.55:
        draw.text((944, 87), "01", font=SMALL_BOLD_FONT, fill=PORTAL_BLUE)
    if orange_progress > 0.55:
        draw.text((1203, 155), "02", font=SMALL_BOLD_FONT, fill=PORTAL_ORANGE)

    draw.text((886, 192), "PORTAL", font=METRIC_FONT, fill=FOREGROUND)
    draw.text((1048, 210), "PLAY / REPLAY", font=SMALL_FONT, fill=MUTED)
    draw.line((1184, 207, 1232, 207), fill=PORTAL_BLUE, width=2)
    draw.line((1208, 207, 1232, 207), fill=PORTAL_ORANGE, width=2)


def render_frame(time_seconds: float) -> Image.Image:
    image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(image)
    draw_grid(draw)

    for left in (24, 443, 862):
        draw.rounded_rectangle(
            (left, 24, left + 394, 236),
            radius=8,
            fill=SURFACE,
            outline=BORDER,
            width=1,
        )

    draw_cube_panel(draw, time_seconds)
    draw_typing_panel(draw, time_seconds)
    draw_portal_panel(draw, time_seconds)
    return image


def save_gif(frames: list[Image.Image]) -> None:
    palette = frames[0].quantize(
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
        if not animation.is_animated or animation.n_frames < 60:
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
    frames = [render_frame(index * FRAME_DURATION_MS / 1000) for index in range(FRAME_COUNT)]
    save_gif(frames)
    render_frame(4.2).save(STILL_PATH, optimize=True)
    verify_outputs()
    print(f"generated {GIF_PATH.relative_to(ROOT)} ({FRAME_COUNT} frames)")
    print(f"generated {STILL_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
