# Illustrations

`experience-timeline.svg` is an original, static employment timeline based only on the
[supplied resume](../../docs/reference/Gaurav_Mahajan_Resume.pdf). It records two
completed roles and month-level dates without implying current employment. The
summaries omit performance metrics and long tool lists so the profile remains modest
rather than becoming a second resume.

The timeline uses the same espresso, crema, caramel, and muted-sage palette as the
personal-interests strip. Its text remains live SVG text, with a title and description
for assistive technology; it has no scripts, external fonts, or remote dependencies.

`practice-strip-espresso.gif` is an original 1280 × 260 animated summary of interests
outside software: speedcubing, typing, and a playful nod to Portal as a favourite
game. Espresso, crema, caramel, and muted sage define the composition. Blue and orange
appear only on the paired Portal gateways.

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
below the fold. The README embeds the GIF directly so GitHub does not replace it with a
static source through a media query. `practice-strip-still.png` remains available as a
complete non-animated reference.

GitHub can still pause animated images when a viewer disables autoplay under
[Accessibility → Motion](https://docs.github.com/en/account-and-profile/how-tos/account-settings/managing-accessibility-settings).
That preference applies across GitHub and cannot be overridden by README markup.

`scripts/generate_practice_strip.py` owns the drawing and animation logic. Run it with
Python 3 and Pillow to regenerate both published files. This repository uses GIF
deliberately because GitHub [supports GIFs in profile READMEs](https://docs.github.com/en/account-and-profile/concepts/personal-profile)
and states that [SVG animation is unsupported](https://docs.github.com/en/repositories/working-with-files/using-files/working-with-non-code-files).
