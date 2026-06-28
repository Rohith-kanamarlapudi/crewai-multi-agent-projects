import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
import os
from dotenv import load_dotenv

load_dotenv()
deepseek_llm = LLM(
    model="deepseek-v4-flash",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

@CrewBase
class Debate:
    """Debate crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def debater(self) -> Agent:
        return Agent(
            config=self.agents_config["debater"],
            llm=deepseek_llm,
            verbose=True
        )

    @agent
    def judge(self) -> Agent:
        return Agent(
            config=self.agents_config["judge"],
            llm=deepseek_llm,
            verbose=True
        )

    @task
    def propose(self) -> Task:
        return Task(
            config=self.tasks_config["propose"]
        )

    @task
    def oppose(self) -> Task:
        return Task(
            config=self.tasks_config["oppose"]
        )

    @task
    def decide(self) -> Task:
        return Task(
            config=self.tasks_config["decide"]
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )