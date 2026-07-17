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
- Avoid legacy image floats, clearing attributes, and layout tables for the hero.
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

The profile uses a restrained lo-fi espresso palette that remains compatible with
GitHub's light and dark themes:

- foreground: GitHub's surrounding text color
- dark surfaces: espresso and roasted-coffee neutrals
- light marks: crema rather than pure white
- secondary linework: warm gray-brown with sufficient contrast
- background: transparent wherever possible
- accents: caramel and muted sage, used sparingly
- Portal pair: subdued blue and orange only for the two gateways
- brand marks: their documented brand colors, used sparingly and only as identifiers

Color must never be the only way an asset communicates structure.

## Imagery and published assets

- Prefer diagrams, geometric studies, and original photography.
- Keep SVGs small, accessible, and free of scripts, external fonts, and embedded data.
- Include a `<title>` and `<desc>` for meaningful SVGs.
- Use SVG only for static vector work on GitHub. When motion is essential, publish one
  optimized repository-owned GIF with a complete still-image companion.
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
- Keep one short, calm cycle with a meaningful completed-state pause; avoid continuous
  movement, flashes, or competing animations.
- Keep the cycle near six seconds and the published file comfortably below GitHub's
  image limits.
- Keep a complete still companion even when the README embeds the GIF directly to avoid
  an unexpected static substitution.

## Explicit exclusions

The profile does not use view counters, contribution snakes, badge walls, downloaded
or generic GIFs, generated headers, streak cards, trophies, auto-generated activity
widgets, decorative statistics cards, or full-page gaming-themed visual treatments.
One repository-owned animation may communicate confirmed personal interests. A game
reference must not reproduce logos, characters, screenshots, slogans, or interface
artwork.
