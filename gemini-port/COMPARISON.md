# Claude vs. Gemini on the same skill, same blind input

Same `SKILL.md`, same references, same template, same `INPUT.md`. The only variables are the model and, for Gemini, the ADK wrapper that feeds the skill files in as the instruction. Claude's run is [`../examples/pega-1to1-ops-manager/OUTPUT.md`](../examples/pega-1to1-ops-manager/OUTPUT.md); Gemini's is [`OUTPUT-gemini.md`](OUTPUT-gemini.md). Both unedited.

**Caveats that matter for reading this.** The Claude run used the *first* version of the skill, before the five fixes described in the main README; the Gemini run used the current version, which includes them (score only described groups, bound departures from the prior, score PM on artifacts, cap metrics, open with a summary). So where Gemini does better on those five items, some credit belongs to the revised skill, not the model. And the Gemini run used `gemini-3.1-flash-lite`, the smallest model the free tier would serve that morning (see "What it took to port"); a Pro-class model would likely produce a longer and more careful plan. This is a comparison of what each stack produced under realistic conditions, not a controlled benchmark.

| | Claude | Gemini |
|---|---|---|
| Model | Claude (claude.ai, skill loaded natively) | `gemini-3.1-flash-lite` via Google ADK 1.18 |
| Skill version | v1 (pre-fixes) | v2 (current) |
| Run date | 2026-10-13 | 2026-10-14 |
| Output length | ~59 KB, ~8,500 words | 7 KB, 1,124 words |
| Validator | fails (no summary, 13 metrics) | fails (missing sections, metrics not a table) |

## Scorecard

Scored against [`GROUND-TRUTH.md`](../examples/pega-1to1-ops-manager/GROUND-TRUTH.md) the same way [`EVALUATION.md`](../examples/pega-1to1-ops-manager/EVALUATION.md) scored the Claude run. "Match" means the output reached the practitioner's conclusion without being told it.

| Check | Ground truth | Claude (v1 skill) | Gemini (v2 skill) |
|---|---|---|---|
| Barrier point for channel managers | Desire | match | match |
| Root causes named for that barrier | skepticism about the model, loss of control, role uncertainty | match (all three) | match: loss of control and role identity named outright; skepticism carried in the stance column and the "shadow targeting" pattern |
| Top structural risk | one sponsor, unit leads report elsewhere | match | match, and it is the #1 risk on the one-page summary |
| Health-check corner ranking | PM highest, CM and sponsorship lowest, all high-risk | match | no ranking: all four corners scored 2 of 5, flat. The three lowest conditions it named (coalition, adoption definition, change work not integrated) overlap two of three with the practitioner's |
| First recommended move | sponsor conversation with a specific ask | match | match: "establish a coalition of LOB marketing leads by [date + 2 weeks]" is the ask, on page one |
| Scored only groups with described impact | one group assessed; four were a working list | no (scored all five) | no (scored all five), despite the v2 instruction |
| Desire score vs. practitioner | 3 | 2 (one point more severe) | 2 (one point more severe), the same call |
| Project management scored on artifacts, not people | no PM, no schedule | no (credited the ops lead) | yes: "phasing defined, but change tasks not yet in roadmap" |
| Metric count and targets | vital few, no placeholder numbers | 13 metrics, placeholder targets | 3 headline metrics (cap respected), but invented targets: "90% by month 9", "<10% override", "30% cycle-time reduction" |
| Opens with a one-page sponsor summary | yes | no | yes, and it is the best part of the output |
| Validator result | pass | fails on summary and metrics | fails: no sponsor roadmap, no people-manager toolkit, judgment-calls heading renamed, metrics as bullets not a table |

Tally on the five substantive diagnosis checks (barrier, root causes, structural risk, health ranking, first move): Claude 5 of 5, Gemini 4 of 5. On the five process-discipline checks the v2 skill added: Claude v1 0 of 5 (by construction), Gemini v2 2 of 5.

## What differed

**Structure compliance.** Gemini kept the section numbering and order of the template but dropped the two sub-sections that take the most work (the sponsor roadmap and the people-manager toolkit), renamed the judgment-calls heading, and rendered the metrics as bullets instead of the table the validator looks for. It treated the template as a guide rather than a contract. Claude followed the template to the letter and then over-filled it. Neither passed the validator, for opposite reasons.

**Diagnosis quality.** On the questions that matter to a sponsor, the two agreed with each other and with the practitioner: Desire is the barrier for channel managers, the single-sponsor-across-units structure is the top risk, and the first move is a sponsor conversation with a specific ask. Where they disagreed, Claude was closer: its health check discriminated between the four corners (and matched the practitioner's ranking); Gemini scored every corner 2 and lost the signal. Gemini also gave LOB leads a Reinforcement score of 3 with nothing in the input to support it, which the skill's "not evidenced = 1" rule should have prevented.

**Register and length.** Gemini's output is something a sponsor could read in five minutes, and its one-page summary is tighter than anything in the Claude run. It also coined a usable phrase, "shadow targeting," for the pattern Claude described in a paragraph (rebuilding the old segments inside the new tool's eligibility rules). The cost is depth: the stakeholder map is a row of two-word cells, the comms plan has four rows, and there is no manager toolkit at all. Claude's plan is the one you would work from; Gemini's is the one you would send upward.

**Invented facts.** Gemini wrote "Prepared 2024-05-23" at the top, a date from nowhere, and put specific numeric targets on every metric where the skill says to leave targets to the group's leader. Claude's v1 run had the same placeholder-target habit (that is why the fix exists) but did not fabricate a date. On a plan that will be read by someone who knows the program, an invented number is worse than a blank.

**Judgment calls.** Both surfaced the same unknowns: which unit leads are passive, which LOB should pilot first, whether the manual path is really retired at go-live. Gemini put two of them on the one-page summary under "What only you can answer," which is the right place for them.

## What it took to port

The skill files were not modified. The ADK agent ([`change_management_agent/agent.py`](change_management_agent/agent.py)) reads `SKILL.md`, every file in `references/`, and the template, concatenates them into one instruction (about 40 KB), and appends a line telling the model that the files it is told to "read" are already present inline. That is the whole adaptation; the skill loaded on the first try.

Getting a response was the hard part, and none of it was about the skill:

- The free tier returned `503 UNAVAILABLE, high demand` on `gemini-flash-latest` and `gemini-3.8-flash` for roughly sixteen hours across two days, through four retries with backoff each time.
- The model ids I started with (`gemini-2.5-flash`, `gemini-2.5-pro`, `gemini-2.0-flash`) returned `404, no longer available to new users`; Google's error message pointed to the 3.x ids.
- `gemini-3.8-pro` returned 404 on the free tier, and `gemini-pro-latest` returned `429` with every per-model free-tier quota at zero and a four-hour retry delay. Pro models are not reachable without billing.
- The run that finally succeeded did so because the runner stopped guessing names: it asks the API which models the key can see, orders them lightest first, and tries each in turn. `gemini-3.1-flash-lite` answered on the first attempt.
- Python 3.9 (the macOS Xcode default) ran the ADK with warnings and without MCP support; the rerun used Python 3.13.

By comparison, the Claude run was one pass with no operational work. That is a statement about the free tier of one platform on two particular days, not about the models, but it is what a practitioner without a cloud budget would hit.

## What I'd tell someone choosing a model for this job

Both models get the diagnosis right when the skill is good, which is the point of writing the skill. The differences are in discipline, not insight: Claude followed the template completely and over-produced; Gemini Flash-Lite summarized well and dropped sections, and it was more willing to invent a number or a date to fill a slot. For a plan a sponsor reads, I would take Gemini's first page and Claude's remaining six sections. For a plan a change lead works from, the Claude output is the one to start from. And if you are evaluating on a free tier, budget a day for the platform to let you run at all; the skill is the easy part.
