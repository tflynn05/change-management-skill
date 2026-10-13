"""ADK agent that loads the change-management skill files as its instruction.

The skill was written for Claude. This agent gives Gemini the same SKILL.md,
references, and template, so the comparison is between models given identical
instructions, not between two different prompts.

Run from the gemini-port/ folder:
    adk run change_management_agent          # interactive
    python run_blind_test.py                 # the blind test, non-interactive
"""
from pathlib import Path

from google.adk.agents.llm_agent import Agent

SKILL_DIR = Path(__file__).resolve().parents[2] / "change-management"


def load_skill_instruction() -> str:
    """Concatenate SKILL.md, every reference, and the template into one
    instruction, in the order the skill tells Claude to read them."""
    parts = [SKILL_DIR.joinpath("SKILL.md").read_text()]
    for ref in sorted(SKILL_DIR.joinpath("references").glob("*.md")):
        parts.append(f"\n\n# REFERENCE FILE: references/{ref.name}\n\n{ref.read_text()}")
    tpl = SKILL_DIR / "templates" / "change-plan.md"
    parts.append(f"\n\n# TEMPLATE FILE: templates/change-plan.md\n\n{tpl.read_text()}")
    parts.append(
        "\n\nYou have every file the skill refers to above. Where the skill says to read a "
        "references/ file, use the matching REFERENCE FILE section. Write the final plan "
        "using the TEMPLATE FILE structure. Do not ask questions; make labeled assumptions."
    )
    return "".join(parts)


root_agent = Agent(
    model="gemini-3.8-flash",  # run_blind_test.py overrides this; swap for a Pro model to compare quality
    name="change_management_agent",
    description="Turns a platform or AI rollout description into a change management plan.",
    instruction=load_skill_instruction(),
)
