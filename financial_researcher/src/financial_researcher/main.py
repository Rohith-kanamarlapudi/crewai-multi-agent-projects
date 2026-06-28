#!/usr/bin/env python
import warnings
import os

from financial_researcher.crew import ResearchCrew
from dotenv import load_dotenv

load_dotenv()

warnings.filterwarnings(
    "ignore",
    category=SyntaxWarning,
    module="pysbd"
)

os.makedirs("output", exist_ok=True)


def run():
    """
    Run the research crew.
    """
    inputs = {
        "company": "Tesla"
    }

    result = ResearchCrew().crew().kickoff(inputs=inputs)

    print("\n\n=== FINAL REPORT ===\n\n")
    print(result.raw)

    print("\n\nReport has been saved to output/report.md")


if __name__ == "__main__":
    run()