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
hold the longer prose; the public page should favor a modest introduction, one verified
work timeline, and one personal visual. Project and writing sections should be added
only after their entries are curated.

## Layout

- Use a simple visual flow that remains legible on mobile.
- Let one original hero establish identity; follow it immediately with a native-text
  statement so the page remains meaningful if images fail.
- A borderless left-aligned portrait may anchor the introduction. Clear its alignment
  explicitly before the first divider or full-width asset.
- Prefer short paragraphs and generous section breaks.
- Keep section headings, dividers, and full-width assets on one consistent center line.
- Give generated assets equal outer padding, aligned panel edges, and a shared corner,
  border, and spacing system.
- Use tables only for genuinely relational information, not for page layout.
- Keep the README useful when images are unavailable.
- Keep employment history to verified roles, dates, and one grounded summary per role.
- Present employment newest-first under `Experience`, using one vertical rail, compact
  nodes, date eyebrows, and aligned cards rather than numbered dashboard widgets.
- Keep one four-logo core stack row; do not add names, badges, or more tools to it.

## Typography

GitHub's native interface typography is the default. SVG assets should use platform
system fonts only when text is unavoidable. Sans-serif type carries role titles and
metrics; monospace is reserved for dates, labels, and small technical annotations.
Do not encode headings or body copy as vector paths.

The writing should use sentence case, restrained punctuation, and direct language.
Avoid slogans, inflated claims, and resume-style keyword lists.

## Color

The generated visual system is dark-first and deliberately cool. It uses restrained
depth rather than decorative color:

- canvas: near-black graphite (`#090D13`) with a slight slate shift (`#0D141D`)
- surfaces: graphite and raised slate (`#101720`, `#151E29`)
- primary type: cool off-white (`#E7EDF4`)
- secondary type: slate gray (`#8E9BAA`)
- borders and guides: low-contrast blue slate (`#2A3747`, `#17212D`)
- accents: muted blue and cyan (`#62B0D5`, `#69C5C3`), used for hierarchy and motion
- Portal pair: blue plus one restrained orange gateway; orange is not a theme accent
- semantic color: the cube retains its six real face colors
- brand marks: their documented colors, used only as identifiers

Gradients may establish quiet depth across a large surface. Glow is limited to a
small active node or portal edge; panels do not receive neon halos. Warm brown, coffee,
and earthy theme treatments are outside this direction.

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
- Use eased state changes: cube transitions cross-fade between validated states,
  keycaps travel down and back smoothly, and gateways scale in without bouncing.
- Keep the first frame complete and intentional because viewer motion preferences may
  pause the GIF. Custom CSS, JavaScript, and hover transitions are not available in a
  GitHub profile README.
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
