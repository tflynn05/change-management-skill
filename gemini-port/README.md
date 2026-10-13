# gemini-port: the same skill, run on Google's stack

This folder runs the change-management skill through Google's [Agent Development Kit (ADK)](https://google.github.io/adk-docs/) with a Gemini model, on the same blind input the Claude version was tested with, so the two can be compared like for like. The skill files are not modified; the ADK agent reads them from `../change-management/` and feeds them in as its instruction.

## Setup

```
cd gemini-port
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp change_management_agent/.env.example change_management_agent/.env   # add your Google AI Studio key
```

## Run the blind test

```
python run_blind_test.py                              # default: gemini-3.8-flash, with fallbacks
python run_blind_test.py --model gemini-3.8-pro --out OUTPUT-gemini-pro.md
```

Each run writes an unedited `OUTPUT-gemini*.md`. Then check structure and score it:

```
python3 ../change-management/scripts/validate_plan.py OUTPUT-gemini.md
```

and fill in `COMPARISON.md`.

## Try it interactively

```
adk run change_management_agent      # terminal
adk web --port 8000                  # browser UI at http://localhost:8000
```

## Notes

- Model ids change; Google retired the 2.x ids for new users in Oct 2026. If a run fails with 404, the error message names the current id. Record the model and the date in `COMPARISON.md`.
- The agent inlines every reference file into the instruction (about 40 KB). A variant that exposes the references as tools, so the model reads them only when the skill says to, would be closer to how Claude loads a skill and is a reasonable follow-up.
- To run on Vertex AI instead of AI Studio, see `.env.example`.
