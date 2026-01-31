#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from report_summarization_crew.crew import ReportSummarizationCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    this function runs the report summarization crew.
    """
    inputs = {
        'topic': 'Software Development and IT support analyst',
    }

    my_crew = ReportSummarizationCrew().crew()

    result = my_crew.kickoff(inputs = inputs)

if __name__ == "__main__":
    run()