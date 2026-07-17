# Design language

## Intent

The profile should read like an engineer's notebook: calm, precise, useful, and built
to age well. Visual choices support the writing and the structure; they do not compete
with them.

## Principles

1. **Information can be visual.** Every visible element should carry meaning or
   establish useful hierarchy; prose is not the only way to communicate substance.
2. **Structure before density.** Prefer a few well-separated sections to a dashboard
   of small widgets.
3. **Principles before tools.** Technologies may explain a project, but they should
   not stand in for an engineering identity.
4. **Original before generic.** Use project-owned diagrams, photographs, and marks;
   avoid stock illustrations and copied visual language.
5. **Durability before novelty.** Avoid assets and services that require constant
   maintenance merely to keep the page rendering correctly.

## README composition

The root documents are the sources of truth:

| Source | Responsibility |
| --- | --- |
| `OVERVIEW.md` | Project brief, confirmed background, and editorial boundaries |
| `profile.md` | Stable biography and personal context |
| `philosophy.md` | Engineering principles and decision-making |
| `now.md` | Dated current focus |
| `links.md` | Verified external destinations |

`README.md` is a concise visual composition of those sources. The supporting documents
hold the longer prose; the public page should favor a strong hero, compact identifiers,
and short editorial lines. Project and writing sections should be added only after
their entries are curated.

## Layout

- Use a single, centered visual flow that remains legible on mobile.
- Let one original hero establish identity; follow it immediately with a native-text
  statement so the page remains meaningful if images fail.
- Prefer short paragraphs and generous section breaks.
- Use tables only for genuinely relational information, not for page layout.
- Keep the README useful when images are unavailable.
- Keep logo rows to four deliberate identifiers; never expand them into inventories.

## Typography

GitHub's native interface typography is the default. SVG assets should use platform
system fonts only when text is unavoidable. Do not encode headings or body copy as
vector paths.

The writing should use sentence case, restrained punctuation, and direct language.
Avoid slogans, inflated claims, and resume-style keyword lists.

## Color

The default palette is neutral and compatible with GitHub's light and dark themes:

- foreground: GitHub's surrounding text color
- secondary linework: middle gray with sufficient contrast in both themes
- background: transparent wherever possible
- accent: one muted accent for original assets
- paired accent: muted blue and orange only when they distinguish the two endpoints
  in the Portal-inspired replay loop
- brand marks: their documented brand colors, used sparingly and only as identifiers

Color must never be the only way an asset communicates structure.

## Imagery and SVGs

- Prefer diagrams, geometric studies, and original photography.
- Keep SVGs small, accessible, and free of scripts, external fonts, and embedded data.
- Include a `<title>` and `<desc>` for meaningful SVGs.
- Prefer transparent backgrounds. When a full-surface background is needed to preserve
  theme-aware contrast, document the exception and verify both light and dark variants.
- Use product logos only as concise, truthful identifiers or navigation. Keep them
  separate, labeled, and sourced; never build a decorative logo wall.
- Monograms and signatures must be based on user-provided initials or source material.

## Accessibility

- Give meaningful images descriptive alternative text.
- Treat decorative images as decorative rather than repeating nearby prose.
- Maintain readable contrast and avoid tiny labels in diagrams.
- Do not rely on animation, hover behavior, or color perception.

## Motion

- Animate only when motion communicates an existing idea rather than decorating space.
- Prefer one short sequence that settles into a complete static state; do not create
  perpetual loops.
- Keep the sequence under five seconds, avoid flashes, and use restrained movement.
- Honor `prefers-reduced-motion` and ensure the still state communicates the same facts.

## Explicit exclusions

The profile does not use view counters, contribution snakes, badge walls, animated
GIFs, generated headers, streak cards, trophies, auto-generated activity widgets,
decorative statistics cards, or full-page gaming-themed visual treatments. A single
personal reference may translate a game mechanic into an original technical diagram;
it must not reproduce logos, characters, screenshots, slogans, or interface artwork.
