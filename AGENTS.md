# AGENTS.md

Rules for coding agents working in the Karya repository. Read this file at the start of every session. Claude Code reads it through the line `@AGENTS.md` in `CLAUDE.md`.

Written to `07_PHASED_IMPLEMENTATION_ROADMAP.md` v0.1 section 20.1 and issued with `docs/HANDOFF.md` v1.0 on 2026-10-24. `docs/HANDOFF.md` is the full brief; this file is the short form you read every session. Lines marked `UPDATE` change at every phase entry.

## 1. What this repository is

Karya is a local-first job search platform for one owner. The plan is fixed in `docs/plan/`:

| Document | Version | Governs |
| --- | --- | --- |
| `00_PRODUCT_AND_SYSTEM_PLAN.md` | 1.5 | Product scope, requirements, architecture |
| `01_SHARED_CONTRACTS_AND_DOMAIN_MODEL.md` | 1.5 | Types, schemas, state machines, terminology |
| `02_SECURITY_AND_THREAT_MODEL.md` | 1.5 | Trust boundaries, mandatory controls |
| `03_CONTROL_PLANE_AND_WORKER_RUNTIME_PLAN.md` | 1.4 | Authority, roles, runs, sources, models, sync |
| `04_DESKTOP_APPLICATION_PLAN.md` | 1.2 | Desktop app on macOS, then Linux and Windows |
| `05_MOBILE_COMPANION_PLAN.md` | 0.4 | Android companion, then iOS |
| `06_DESIGN_SYSTEM_AND_UX_PLAN.md` | 0.1 | Views, flows, components, tokens, copy |
| `07_PHASED_IMPLEMENTATION_ROADMAP.md` | 0.1 | Phases, gates, allocation of acceptance criteria |

All eight were accepted for implementation by the owner on 2026-10-24. The status rows inside `00` to `06` still say that changes await review, and the revision pass of `07` section 19 has not run; `07` section 4 is the reconciliation and it is binding. When two documents disagree, follow `07` section 4. If section 4 does not resolve it, stop (section 4 of this file, condition 9).

## 2. Current phase

`UPDATE` Current phase: **`P0` Foundations and platform proof** (`07` section 8.1).

`UPDATE` Owner hours available per week (`OQ-702`): _to be filled in before `P0` starts._
`UPDATE` Repository hosting and visibility, and whether CI runs on hosted runners (`OQ-703`): _to be filled in before `P0` starts._

1. Build only what the current phase's specification in `07` section 8 includes. Its "Excluded" row is binding.
2. Every acceptance criterion allocated to the phase (`07` sections 16 to 18) must pass, and every criterion of earlier phases must keep passing.
3. A refinement of the phase's tasks is proposed at entry review and approved by the owner before work starts (`07` section 14.1 step 1).
4. Spike code from `P0` lives on `spike/<EXP>` branches and reaches `main` only after review.

## 3. Never

1. Never edit anything under `docs/plan/`. A needed change to an approved document goes to the owner as a conflict row in the phase report.
2. Never change an approved contract, decision, or control to make code work. Stop and report instead.
3. Never put real candidate data in the repository, CI, fixtures, phase reports, issues, or this conversation (section 5).
4. Never contact a real employer application form, and never write a code path that could submit to a real employer without the gates of the current phase.
5. Never contact real job sources or model providers before the phase that authorizes it.
6. Never use a literal color, size, radius, shadow, or duration in component code (section 6).
7. Never load fonts, scripts, or styles from a CDN in the product.
8. Never disable a security test, a negative test, or a CI gate to get a green build.

## 4. Stop conditions

Stop work, write down what happened, and wait for the owner when any of these occurs (`07` section 15.2):

1. A role starts without its required confinement, or any canary is readable from a role.
2. A required negative test or a `P0` security control (`02` section 8) fails and the fix is not within the phase's scope.
3. Real candidate data appears, or would need to appear, in the repository, CI, a fixture, a phase report, or a coding-agent conversation.
4. A change to an approved contract, decision, or control would be needed.
5. Any code path could submit to a real employer without the gates of the current phase.
6. A test would contact a real application form.
7. Measured owner hours for the phase exceed 150 percent of the upper estimate.
8. An experiment's result has no pre-decided outcome.
9. An upstream document and `07` disagree in a way `07` section 4 does not resolve.

The phase specification may add its own stop conditions (`07` section 8, "Stop conditions" row).

## 5. Data rules

1. `fixtures/` contains synthetic data only. Label every invented person, employer, and posting as synthetic.
2. The owner's real evidence, claims, answers, and packages exist only in the `reference` installation on the owner's devices.
3. Real postings used for evaluation stay in an encrypted folder outside the repository and are referenced by digest.
4. To debug a real-data failure, ask the owner to reproduce it with a synthetic fixture first.
5. Canary strings planted in the owner's real profile must never appear in the repository or CI artifacts (`07` `AC-704`).

## 6. Design rules

1. `design/tokens/karya.tokens.json` is the only source of design values. Components use the generated token variables (CSS custom properties on the desktop, `KaryaTheme` on Android). A lint rule rejects literals.
2. `06` text governs every view, flow, component, state, and string. The mockups in `design/reference/` are non-normative.
3. **Before building a view:** open its screenshot in `design/reference/screens/` (if one exists; the board table is in `design/reference/README.md`) and read the `06` sections it lists.
4. **After building a view:** take a screenshot of the built view at the board's frame size, compare it with the reference and with `06`, and record differences in the phase report. A difference that follows `06` is correct; any other difference is a defect.
5. Copy comes from `06` (strings and the copy lint). Do not invent user-facing text where `06` gives it.
6. Status is never color alone: icon and word every time (`06` section 6.3).
7. Respect Reduce Motion, Reduce Transparency, increased contrast, and the safety-control rule that stop, pause, lock, and decline act on press (`06` `ADR-603`).
8. Run the contrast check after any token change; a token change is a reviewed change with a before and after contrast report.

## 7. Working method

1. Start each session by reading this file, the current phase's specification in `07` section 8, and the latest report in `docs/phase-reports/`.
2. Keep module boundaries (`03` section 6.1); import-linter and crate boundaries enforce them.
3. Generated files (schemas, OpenAPI, TypeScript types, token outputs) are committed and must match regeneration.
4. Each phase adds its tests next to its code and its fixtures under `fixtures/`.
5. Implementation decisions that no document makes (library choices within an approved category, tooling) are recorded as ADRs in `docs/adr/`, numbered from `ADR-801`, and reported in the phase report.
6. When unsure whether something is in scope, it is not. Ask.

## 8. Phase report

At the end of the phase, write `docs/phase-reports/Pn.md` with the template in `07` section 14.2: entry criteria, scope delivered and not delivered, every allocated acceptance criterion with result and evidence, experiments and decisions, security gate evidence, tests, demonstration, deviations and conflicts, risks, effort, handover, and the request to the owner. Report partial passes as partial. The owner approves; the approved commit is tagged `phase-Pn-approved`.
