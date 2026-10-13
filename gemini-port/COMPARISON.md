# Claude vs. Gemini on the same skill, same blind input

Same `SKILL.md`, same references, same template, same `INPUT.md`. The only variable is the model (and, for Gemini, the ADK wrapper that feeds the skill files in as the instruction). Claude's run is `../examples/pega-1to1-ops-manager/OUTPUT.md`; Gemini's is `OUTPUT-gemini.md`. Both unedited.

Model versions: Claude: _fill in_. Gemini: _fill in (`gemini-flash-latest` resolves to … on the run date)_. Run date: _fill in_.

## Scorecard

Score each against `../examples/pega-1to1-ops-manager/GROUND-TRUTH.md`, the same way `EVALUATION.md` scored the Claude run. "Match" means the output reached the same conclusion as the practitioner without being told.

| Check | Ground truth | Claude | Gemini |
|---|---|---|---|
| Barrier point for channel managers | Desire | match | |
| Root causes named for that barrier | skepticism about the model, loss of control, role uncertainty | match (all three) | |
| Top structural risk | one sponsor, unit leads report elsewhere | match | |
| Health-check corner ranking | PM highest, CM and sponsorship lowest, all high-risk | match | |
| First recommended move | sponsor conversation with a specific ask | match | |
| Scored only groups with described impact | one group assessed; four were a working list | no (scored all five) | |
| Desire score vs. practitioner | 3 | 2 (one point more severe) | |
| Project management scored on artifacts, not people | no PM, no schedule | no (credited the ops lead) | |
| Metric count and targets | vital few, no placeholder numbers | 13 metrics, placeholder targets | |
| Opens with a one-page sponsor summary | yes | no | |
| Validator (`validate_plan.py`) result | pass | fails on last two | |

## What differed

_Fill in after the run. Useful angles:_

- **Structure compliance.** Did Gemini follow the template section order? Did it respect the three-question cap and make labeled assumptions, or did it ask?
- **Diagnosis quality.** Where it disagreed with Claude, which one was closer to the ground truth?
- **Register.** Which plan could a sponsor read? Length, directness, hedging.
- **Judgment calls.** Did it surface the same unknowns (which unit leads are passive, which unit pilots first)?
- **Failure modes.** Where did each model invent evidence the input did not contain?

## What it took to port

_Fill in. For example: no changes to the skill files; the ADK agent concatenates them into the instruction; the only decisions were model choice and how to hand over the reference files (inline vs. tools). Note anything that broke._

## What I'd tell someone choosing a model for this job

_One paragraph, after the run._
