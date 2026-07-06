# DESIGN.md — Template Gallery Showreel

## Style Prompt

Dark, premium, Linear-Vercel engineering aesthetic. The video showcases 12 production-ready template previews as a single frame, with each template's accent color and UI elements animating in. Composition is grid-locked with a single emerald accent. The mood is precise and technical, like a product launch reel for design systems.

## Colors

| Role            | Hex      | Use                                                  |
| --------------- | -------- | ---------------------------------------------------- |
| `bg`            | `#0a0a0f`| Canvas background for every scene                    |
| `surface`       | `#16161a`| Card surfaces, panels                                |
| `surface-2`     | `#1c1c21`| Elevated panels                                      |
| `text`          | `#fafafa`| Primary text, large displays                         |
| `text-muted`    | `#a1a1aa`| Labels, descriptions                                 |
| `text-faint`    | `#52525b`| Meta, timestamps, monospace tags                     |
| `accent`        | `#10b981`| Single accent — emerald. Industry badges, active CTAs |
| `accent-bright` | `#34d399`| Accent highlights, glow                              |

Template accent colors (per template, used in their preview frame only):
- `crm` `#6366f1`, `sale` `#f97316`, `bazi` `#dc2626`, `numerology` `#06b6d4`
- `blog` `#10b981`, `portfolio` `#ec4899`, `food-delivery` `#ef4444`, `edu-tutor` `#3b82f6`
- `beauty-spa` `#ec4899`, `fitness` `#22c55e`, `realestate` `#f59e0b`, `travel` `#06b6d4`

## Typography

- **Display**: `Geist` 700-900, 80-160px headlines with -0.04em letter-spacing
- **Body**: `Geist` 350-400, 24-32px, line-height 1.45
- **Mono**: `Geist Mono` 500, 16-22px for tags, codes, meta
- Tabular numbers for any stacked digits (`font-variant-numeric: tabular-nums`)

## Motion Rules

- **Pace**: Medium energy. Each template gets ~3s of screen time in the gallery, with 1s of focus on its details
- **Entrances**: `power3.out` for primary content, `power2.out` for secondary, `expo.out` for stat counters
- **Ambient**: Each preview has slow breathing scale 1.0→1.015 over 4s, ease `sine.inOut`
- **Transitions**: `push slide` primary (0.4s, `power2.inOut`) for most scene changes; `cinematic zoom` for the final hero frame
- **No exit animations** before transitions — the transition IS the exit

## What NOT to Do

- No gradient text (`background-clip: text`)
- No cyan-on-dark or purple-blue gradients (already banned from palette)
- No identical card grids of the same size — vary each template card's accent + micro-layout
- No full-screen linear gradients (H.264 banding) — use solid `#0a0a0f` with localized radial glow
- No `repeat: -1` — every animation has a finite end
- No center-everything layouts — lead the eye to the template card area, not the title
- No emoji in any output
- No use of banned fonts (Inter, Roboto, Open Sans, Noto Sans, Poppins, Syne, etc.)
- Do not invent new accent colors mid-composition — every hue is declared above
