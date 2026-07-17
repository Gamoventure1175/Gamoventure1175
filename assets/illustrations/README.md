# Illustrations

`practice-strip.svg` is an original 1280 × 260 animated summary of interests outside
software: speedcubing, typing, and a playful nod to Portal as a favourite game. It is
built entirely from SVG primitives, uses no external assets, and adapts to GitHub
light and dark themes.

The illustration carries the exact confirmed figures—8.76-second personal best,
10–15-second typical solves, and 90+ WPM—so the public README can remain concise.
The third panel uses paired gateways and a replay loop to communicate affection rather
than achievement. It does not reproduce Valve artwork, logos, characters, or slogans.

## Motion

One coordinated 4.8-second sequence runs when the visitor has not requested reduced
motion:

- a cube with white, yellow, red, orange, blue, and green stickers resolves from a
  scramble into three uniformly solved visible faces;
- the letter keys and spacebar tap in a short, irregular typing burst;
- the blue gateway opens first, followed by the warm-gold gateway and replay path.

The sequence runs once and holds its finished state. `prefers-reduced-motion: reduce`
disables every animation, leaving a solved cube, resting keyboard, and open gateways.
The complete static composition also remains available when animation is unsupported.

GitHub accepts repository-relative SVG images, but its documentation does not promise
SVG animation support. Treat the motion as a progressive enhancement and verify it on
the published profile; the still state is the supported fallback.
