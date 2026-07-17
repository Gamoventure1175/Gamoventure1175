# Illustrations

`practice-strip.gif` is an original 1280 × 260 animated summary of interests outside
software: speedcubing, typing, and a playful nod to Portal as a favourite game. Its
dark neutral surface is designed to sit cleanly in either GitHub theme, with blue and
orange used as paired accents rather than a dominant wash.

The illustration carries the exact confirmed figures—8.76-second personal best,
10–15-second typical solves, and 90+ WPM—so the public README can remain concise.
The third panel uses paired gateways and a replay loop to communicate affection rather
than achievement. It does not reproduce Valve artwork, logos, characters, or slogans.

## Motion and generation

One restrained six-second cycle communicates the three interests:

- a modeled cube with white, yellow, red, orange, blue, and green stickers follows a
  fixed inverse move sequence from scramble to solved;
- the letter keys and spacebar tap at a fast but readable pace;
- the blue gateway opens first, followed by the orange gateway and replay path.

The sequence holds its completed state before a short reset so motion is not missed
below the fold. `practice-strip-still.png` shows that completed state, and the README
selects it for visitors who request reduced motion.

`scripts/generate_practice_strip.py` owns the drawing and animation logic. Run it with
Python 3 and Pillow to regenerate both published files. This repository uses GIF
deliberately because GitHub [supports GIFs in profile READMEs](https://docs.github.com/en/account-and-profile/concepts/personal-profile)
and states that [SVG animation is unsupported](https://docs.github.com/en/repositories/working-with-files/using-files/working-with-non-code-files).
