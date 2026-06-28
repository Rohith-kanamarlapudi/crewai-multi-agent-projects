from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from pydantic import BaseModel, Field
from typing import List

from .tools.push_tool import PushNotificationTool

import os
from dotenv import load_dotenv

load_dotenv()

deepseek_llm = LLM(
    model="deepseek-v4-flash",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)


class TrendingCompany(BaseModel):
    name: str = Field(description="Company name")
    ticker: str = Field(description="Stock ticker symbol")
    reason: str = Field(description="Reason this company is trending in the news")


class TrendingCompanyList(BaseModel):
    companies: List[TrendingCompany]


class TrendingCompanyResearch(BaseModel):
    name: str
    market_position: str
    future_outlook: str
    investment_potential: str


class TrendingCompanyResearchList(BaseModel):
    research_list: List[TrendingCompanyResearch]


@CrewBase
class StockPicker:
    """StockPicker crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def trending_company_finder(self) -> Agent:
        return Agent(
            config=self.agents_config["trending_company_finder"],
            llm=deepseek_llm,
            tools=[SerperDevTool()],
            memory=False,
            max_iter=5,
            verbose=True,
        )

    @agent
    def financial_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["financial_researcher"],
            llm=deepseek_llm,
            tools=[SerperDevTool()],
            memory=False,
            max_iter=5,
            verbose=True,
        )

    @agent
    def stock_picker(self) -> Agent:
        return Agent(
            config=self.agents_config["stock_picker"],
            llm=deepseek_llm,
            tools=[PushNotificationTool()],
            memory=False,
            max_iter=5,
            verbose=True,
        )

    @task
    def find_trending_companies(self) -> Task:
        return Task(
            config=self.tasks_config["find_trending_companies"]
        )

    @task
    def research_trending_companies(self) -> Task:
        return Task(
            config=self.tasks_config["research_trending_companies"]
        )

    @task
    def pick_best_company(self) -> Task:
        return Task(
            config=self.tasks_config["pick_best_company"]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the StockPicker crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            memory=False,
        )