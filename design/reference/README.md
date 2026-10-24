# Karya design reference

Status: draft, prepared 2026-10-02 with `06_DESIGN_SYSTEM_AND_UX_PLAN.md` v0.1 and `07_PHASED_IMPLEMENTATION_ROADMAP.md` v0.1, both awaiting owner approval.

This folder lets a coding agent (Claude Code, Codex, or another) see what the views described in `06` should look like. It contains twelve mockup boards as standalone HTML, a PNG screenshot of each, and the scripts to make the fonts local and to re-render the screenshots.

## 1. Rules of use

1. **`06` text governs.** When a board and `06` disagree, `06` is right and the board is wrong. Report the difference in the phase report; do not copy the board.
2. **Values come only from `design/tokens/karya.tokens.json`.** The boards contain literal colors, sizes, and shadows because they are mockups. Component code never copies a literal from a board; it uses the generated token variables (`06` `ADR-610`, `07` `AC-705`).
3. **The boards are non-normative** for layout details, copy, and data. They are normative only in that their colors, type, space, and shape values were taken from the token table of `06` section 6.
4. **All content is placeholder.** Employers ("Example Robotics", "Halden Interactive", and the rest), dates, scores, and counts are invented. Do not reuse them as fixtures without labeling them synthetic.
5. **Before building a view:** open its screenshot from `screens/` and the `06` sections listed in section 3 below. **After building it:** take a screenshot of the built view at the same size and compare. Differences that follow `06` are fine; differences that do not are defects.
6. **Boards cover twelve states, not the product.** A view without a board is built from `06` text alone.
7. `P0` of `07` produces the final token pipeline (CSS variables for the desktop webview, Kotlin theme for Android) and the contrast report. Until then, this token file is the reviewed input to that pipeline, not generated output.

## 2. Folder contents

| Path | What it is |
| --- | --- |
| `../tokens/karya.tokens.json` | Design tokens in Design Tokens Community Group JSON: `ref` (palette, font families), `sys` (both themes, increased contrast, type for desktop and Android, space, shape, elevation, glass, motion, breakpoints, layout), `cmp` (empty by design) |
| `html/*.html` | The twelve boards as standalone HTML. No scripts. Each board is a fixed-size frame; open it in a browser |
| `html/fonts.css` | Font loading for the boards. Ships in its online form (Google Fonts import). `fonts/fetch-fonts.sh` replaces it with embedded fonts |
| `fonts/fetch-fonts.sh` | Downloads the four OFL families and rewrites `html/fonts.css` with embedded fonts so the boards work offline |
| `fonts/fonts.online.css` | Copy of the online `fonts.css`, restored with `fetch-fonts.sh --online` |
| `screens/*.png` | Screenshots of the boards at 2x scale. **See section 4: these were rendered with stand-in fonts** |
| `boards.json` | Board names, titles, and frame sizes; read by `tools/render_screens.py` |
| `../../tools/render_screens.py` | Re-renders the screenshots with Playwright |

## 3. Boards and the `06` identifiers they illustrate

| Board | Title | Frame (CSS px) | Theme | Illustrates | Read in `06` |
| --- | --- | --- | --- | --- | --- |
| `Main` | Token specimen, Limestone | 1440 x 3391 | Limestone | Palette, roles, type scale, space, shape, elevation, status chips | Section 6 (all), section 6.3 |
| `Tokens-Obsidian` | Token specimen, Obsidian | 1440 x 3391 | Obsidian | The same specimen in the dark theme | Section 6 (all), section 6.3 |
| `AppMark` | App mark, three stroke weights | 1400 x 620 | Limestone | Mark construction and the stroke-weight choice | `ADR-609`, `OQ-601` |
| `Desktop-Today` | Today | 1440 x 900 | Limestone | Home view, run status strip, needs-you list, new jobs table | `DV-618` |
| `Desktop-JobDetail` | Job detail | 1680 x 1000 | Limestone | Wide window class with the Sūtra inspector column | `DV-620`, `CMP-619`, `CMP-620`, `CMP-627` |
| `Desktop-PackageReview` | Package review | 1440 x 900 | Limestone | Package review with claim grounding | `DV-622`, `CMP-621`, `CMP-626` |
| `Desktop-RelaySheet` | Copy-and-paste step | 1440 x 960 | Limestone | Relay exchange sheet (R2) | `DV-621`, `CMP-632`, `CMP-633` |
| `Desktop-Lock-Obsidian` | Karya locked | 1440 x 900 | Obsidian | Lock screen with visible Yantra construction | `DV-601`, `CMP-639` |
| `Android-Home` | Android home | 390 x 844 | Limestone | Phone home, run dock | `MS-503`, `CMP-631` |
| `Android-CardTriage` | Android card triage | 390 x 844 | Limestone | Swipe triage of job cards | `MS-506`, `ADR-607` |
| `Android-StopWaiting` | Android stop status, waiting | 390 x 844 | Limestone | Stop sent, waiting for the Mac to confirm | `MS-504`, `05` `ADR-513`, `05` section 32.8 |
| `Android-StopNotConfirmed-Obsidian` | Android stop not confirmed | 390 x 844 | Obsidian | Stop accepted by the server but not confirmed by the Mac | `MS-504`, `05` `ADR-513`, `05` section 32.8 |

The same twelve boards, rendered with the true fonts, are on the design canvas artifact made during `06` drafting.

## 4. Fonts and the screenshot limitation

The session that produced this bundle had no access to any font download source, so:

1. `html/fonts.css` ships in its online form. With internet access, the boards render with EB Garamond, Instrument Sans, JetBrains Mono, and Noto Serif Devanagari.
2. `screens/*.png` were rendered **with stand-in fonts**: Lora for EB Garamond, Inter for Instrument Sans, DejaVu Sans Mono for JetBrains Mono, FreeSerif for Noto Serif Devanagari. Colors, layout, sizes, and spacing are exact; letterforms and text widths are not. Inter has no width axis, so text set at `font-stretch: 88%` (the `sys.type.table` role) is wider than intended, and a few labels wrap that would not wrap with Instrument Sans (for example "Protection and workers" in the navigation of `Desktop-Today`).
3. To replace them with exact screenshots, run once on your own Mac:

```sh
cd design/reference/fonts && bash fetch-fonts.sh        # downloads fonts, embeds them in html/fonts.css
cd ../../.. && pip install playwright && python3 -m playwright install chromium
python3 tools/render_screens.py                          # rewrites design/reference/screens/*.png
```

The download paths in `fetch-fonts.sh` follow the google/fonts repository layout but were not verified from this session. If a download fails, the script stops and says which file to get from fonts.google.com; then run `bash fetch-fonts.sh --embed-only`.

The fonts are SIL Open Font License 1.1. The script also downloads each family's `OFL.txt`. The product bundles its fonts itself (`06` section 6.4.1, no CDN); this folder's font handling is for the reference boards only.

## 5. Token file notes

1. **Names.** `06` writes roles with dots (`sys.color.surface.sunken`, `sys.color.error` / `container` / `on.container`). In JSON a token cannot also be a group, so multi-part role names use hyphens inside the theme group: `sys.limestone.color.surface-sunken`, `sys.obsidian.color.on-error-container`. Generated CSS variables follow the same names without the theme: `--sys-color-surface-sunken`, with the theme selected by an attribute or media query.
2. **Themes.** `sys.limestone` and `sys.obsidian` hold the same role names. `sys.increased-contrast.<theme>` holds only the overrides of `06` section 6.2.4.
3. **Aliases.** A role whose value is in the reference palette refers to it (`{ref.color.rust.600}`); roles with values outside the palette (containers, selection, fit track, on-primary) carry the hex directly, as `06` section 6.2.2 does.
4. **Android type** sizes are in sp; the file records them in the `fontSize` field with a `px` suffix for tool compatibility and marks the unit in `$extensions.app.karya.unit`.
5. **Format version.** Colors are hex strings and dimensions are strings such as `"16px"`, the form most token tools accept today. My understanding is that the stable 2025 edition of the Design Tokens format also defines object forms for colors and dimensions; `P0` chooses the pipeline and may convert mechanically. This is an implementation choice to record as an `ADR-801`-range decision, not a design change.
6. **Verification done.** Every alias resolves. The WCAG contrast ratios recomputed from this file match every value in `06` section 6.2.3 for both themes (for example `text.tertiary` 4.69 and 5.99, `fit` 4.52 and 7.16, `border.control` 3.32 and 3.89).
