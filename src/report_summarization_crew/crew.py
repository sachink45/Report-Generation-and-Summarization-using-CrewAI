from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.tasks.task_output import TaskOutput
from typing import List, Any


# define the crew base class
@CrewBase
class ReportSummarizationCrew():
    

    # define the datatypes of agents and tasks
    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # goardrail for report summarization
    def validate_word_count_for_summary(self, result : TaskOutput) -> tuple[bool, Any]:
        try:
            word_limit = 400
            # extract str output
            result : str = result.raw.strip()
            word_count : int = len(result.split(" "))
            if word_count > word_limit:
                return (False, "Summary exceeds the word limits of 300, please regenarate the report again with in the word limit")
            return (True, result)
        except Exception as e:
            print('error :', e)    
    

    
    # define agents 
    @agent
    def report_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['report_generator'], # type: ignore[index]
            verbose=True
        )

    @agent
    def report_summarization(self) -> Agent:
        return Agent(
            config=self.agents_config['report_summarization'], # type: ignore[index]
            verbose=True
        )

   
    @task
    def report_genation_task(self) -> Task:
        return Task(
            config=self.tasks_config['report_genation_task'], output_file = "reports/report.md" # type: ignore[index]
        )

    @task
    def report_summarization_task(self) -> Task:
        return Task(
            config=self.tasks_config['report_summarization_task'], # type: ignore[index]
            output_file="reports/report_summary.md",
            guardrail = self.validate_word_count_for_summary,
            guardrail_max_itr = 3
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
