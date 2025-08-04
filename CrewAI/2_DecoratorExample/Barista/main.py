from dotenv import load_dotenv
import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

load_dotenv()


@CrewBase
class LePetitCafeCrew:
    """The cosiest coffee shop's crew"""

    def __init__(self, customer_order):
        self.customer_order:str = customer_order
        self.agents_config: str = 'agents.yaml'
        self.tasks_config: str = 'tasks.yaml'
        self.llm_openai = LLM(
            model=os.getenv("MODEL"),
            api_key=os.environ.get(os.getenv("OS_API_KEY_VAR")),
            base_url=os.getenv("API_ENDPOINT"),
            api_version=os.getenv("API_VERSION")
        )

    @agent
    def agent_order_taker(self) -> Agent:
        return Agent(
            config=self.agents_config['agent_order_taker'],
            llm=self.llm_openai
        )

    @agent
    def agent_coffee_maker(self) -> Agent:
        return Agent(
            config=self.agents_config['agent_coffee_maker'],
            llm=self.llm_openai
        )

    @agent
    def agent_till_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['agent_till_manager'],
            llm=self.llm_openai
        )

    @task
    def task_order_taker(self) -> Task:
        # print(self.tasks_config)
        # print(self.tasks_config['task_order_taker'])
        task_order_taker_amended = self.tasks_config['task_order_taker'].copy()
        task_order_taker_amended["description"] = task_order_taker_amended["description"].format(
            user_input=self.customer_order
        )
        return Task(
            config=task_order_taker_amended,
            agent=self.agent_order_taker()
        )

    @task
    def task_coffee_maker(self) -> Task:
        return Task(
            config=self.tasks_config['task_coffee_maker'],
            agent=self.agent_coffee_maker()
        )

    @task
    def task_till_manager(self) -> Task:
        return Task(
            config=self.tasks_config['task_till_manager'],
            agent=self.agent_till_manager()
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Barista crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )


if __name__ == "__main__":
    user_input = input("Enter your coffee order: \n")
    LePetitCafeCrew(user_input).crew().kickoff()
