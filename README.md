# change-management: a Claude skill for platform rollouts

Give it a description of a platform, tool, or AI rollout. It returns a change management plan: a stakeholder and resistance map, an ADKAR-style readiness assessment with the barrier point for each group, a communications and training plan sequenced to that assessment, the adoption metrics to track, and a list of the judgment calls only an insider can make.

It encodes two things: the structure of a widely used individual-change model, and what I learned leading operations for an enterprise AI decisioning rollout where the technology worked and adoption was the hard part. Then it was tested blind against that rollout, and the places it was wrong were fed back into the skill. The test and the evaluation are in [`examples/pega-1to1-ops-manager/`](examples/pega-1to1-ops-manager/).

Built by [Tim Flynn](https://www.linkedin.com/in/tim-flynn), Prosci® Certified Change Practitioner. I led operations and marketing readiness for an enterprise AI decisioning rollout across 15+ lines of business, and this skill is what I wished I had on day one.

## What it produces

| Section | What it answers |
|---|---|
| One-page summary | What the sponsor needs to read: barrier per group, top three risks, the ask, next three actions |
| Stakeholder and resistance map | Who has to work differently, how much, what they will probably do about it, and why; who they read sponsorship from |
| Readiness assessment | Awareness, Desire, Knowledge, Ability, Reinforcement scored 1 to 5 per group, with evidence; the first element at 3 or below is where the effort goes |
| Project health check | Success definition, sponsorship, project management, and change management, scored from what is actually evidenced |
| Communications and training plan | Sequenced from each group's barrier point, with the right sender for each message, plus a sponsor roadmap, a people-manager toolkit, and an AI trust-building track |
| Adoption metrics | Speed, utilization, and proficiency per group; a one-sentence definition of "adopted"; the link from each metric to a business outcome the sponsor already tracks |
| Judgment calls | Every assumption the plan rests on, and the decisions a description cannot settle |

The operating principles are in [`change-management/SKILL.md`](change-management/SKILL.md). The two that do the most work:

- **Awareness is rarely the barrier on an AI rollout.** Experienced practitioners know the change is coming. They stall at Desire (trust, control, role identity) and Ability. The skill starts there.
- **Sponsor consistency across business units is the strongest predictor of adoption.** Where one platform goes to several units, the plan maps every unit leader and treats a passive one as the top risk.

## What the output looks like

The opening of the blind-run plan, unedited, to show the register it writes in:

> **Where we are.** The description reads as planning stage, at or just after kickoff, with first LOB go-live around month 6. The plan therefore front-loads the diagnostics and the sponsor-coalition work; the communications calendar is keyed to each LOB wave's go-live so it survives date changes. The technology is not the risk here. The risk is that experienced marketers who built and own their own targeting logic are being asked to hand the targeting decision to a model, in several LOBs whose leaders do not report to the sponsor, in an organization whose last several martech rollouts had mixed adoption.

The full plan is [`examples/pega-1to1-ops-manager/OUTPUT.md`](examples/pega-1to1-ops-manager/OUTPUT.md). Note that it predates the one-page-summary and metrics-cap changes described under [The test](#the-test); the current skill produces a shorter plan that opens with the summary.

## Install

This is an [Agent Skill](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview): a folder with a `SKILL.md` and supporting files. Any Claude surface that loads skills can use it.

**Claude Code:** copy or symlink the `change-management/` folder into `.claude/skills/` in your project (project-scoped) or `~/.claude/skills/` (user-scoped). Claude loads it when a rollout comes up, or invoke it directly with `/change-management`.

**Claude.ai:** zip the `change-management/` folder and upload it under Settings, Capabilities, Skills.

**Claude API:** upload the folder with the Skills API and reference it in your request. See the docs link above for the current mechanics.

## Use

Describe the rollout the way a program lead would at planning stage. The skill works best when the description covers:

- what is being rolled out and how it is phased
- the business reason and the cost of not changing
- what changes in each impacted group's daily work
- who the sponsor is and who leads each unit that must adopt
- the timeline, the organization's history with past changes, and the measures the business already uses
- what is algorithmic about the change: what a model or rule now decides that a person decided before

[`examples/pega-1to1-ops-manager/INPUT.md`](examples/pega-1to1-ops-manager/INPUT.md) is a worked input. If something is missing, the skill makes a labeled assumption and lists it under judgment calls rather than stalling.

You can also ask for one component ("just the stakeholder map"); the skill still runs the diagnosis underneath because the components depend on each other.

To check a plan's structure:

```
python3 change-management/scripts/validate_plan.py path/to/plan.md
```

It confirms every section is present and in order, every group in the stakeholder map has a readiness row, the metrics table stays at the vital few with an owner and a business outcome for each, and the judgment-calls list is not empty.

## The test

I ran the first version blind. A fresh model instance got `SKILL.md`, its references, and a planning-stage description of the Pega 1:1 Operations Manager rollout at a large US financial services company (AI-driven next-best-action decisioning replacing hand-built segment campaigns across lines of business), and nothing else. Its output is [`OUTPUT.md`](examples/pega-1to1-ops-manager/OUTPUT.md), untouched.

Then I compared it with what I actually found running the project health check and the readiness assessment on that rollout during my Prosci Change Practitioner certification, and with what I observed leading it ([`GROUND-TRUTH.md`](examples/pega-1to1-ops-manager/GROUND-TRUTH.md)).

**Where it was right** ([`EVALUATION.md`](examples/pega-1to1-ops-manager/EVALUATION.md) has the detail):

- Same barrier point for channel managers (Desire), for the same three reasons I observed: skepticism about the model, loss of control, uncertainty about the role.
- Same top structural risk: one sponsor for a multi-unit rollout where the unit leads report elsewhere, so adoption will be uneven wherever the unit lead is passive.
- Same ranking of the four health-check corners and the same three lowest conditions: no coalition aligned on success, no adoption targets separate from delivery milestones, no owner after the project team leaves.
- Same first move I chose for my certification presentation: a sponsor conversation with a specific ask.

**Where it needed my judgment:**

- It treated my unconfirmed list of impacted groups as fact and scored all of them.
- It scored Desire one point more severe than I did, because the description was vivid.
- It credited project management for the existence of an operations lead; my assessment said no project manager, no schedule.
- It could not know which unit leaders were passive or which unit should pilot first; it correctly said "find out."
- It wrote thirteen metrics with placeholder targets that read as recommendations, and a plan too long for the sponsor to read.

Five of those became changes to the skill: score only groups whose impact is described, bound departures from the prior to one point without direct evidence, score project management on artifacts rather than people, cap the metrics at eight with a headline three and no placeholder numbers, and open every plan with a one-page summary. The strict validator fails the original blind output on exactly the last two.

## Repository layout

```
change-management/            the skill
  SKILL.md                    workflow and operating principles
  references/                 loaded step by step: stakeholder map, readiness, health check, comms and training, metrics
  templates/change-plan.md    output template
  scripts/validate_plan.py    structural check for a finished plan
examples/pega-1to1-ops-manager/
  INPUT.md                    the rollout description fed to the blind run
  OUTPUT.md                   the blind run's plan, unedited
  GROUND-TRUTH.md             what the assessments and the rollout actually showed
  EVALUATION.md               right versus judgment, and the skill changes that followed
gemini-port/                  the same skill run through Google ADK + Gemini, with a comparison
LICENSE                       MIT
```

## Gemini port

[`gemini-port/`](gemini-port/) runs the same skill files through Google's Agent Development Kit with a Gemini model, on the same blind input, so the two models can be compared like for like. See [`gemini-port/COMPARISON.md`](gemini-port/COMPARISON.md).

## Scope and attribution

The skill applies the publicly described structure of the ADKAR model (Awareness, Desire, Knowledge, Ability, Reinforcement) and the common practitioner view of project health across sponsorship, project management, and change management. ADKAR is a registered trademark of Prosci Inc. This project is not affiliated with or endorsed by Prosci; it does not reproduce Prosci's licensed materials, assessments, or templates. The readiness questions, health-check questions, resistance patterns, and plan structure are my own.

The example uses a real rollout. It contains my own assessment results and observations at the level of a case study, completed as certification coursework after my time on the program ended. It contains no customer data, no colleague names, and no internal figures, and it describes conditions of the program rather than the performance of any individual.

## License

MIT. See [`LICENSE`](LICENSE).
