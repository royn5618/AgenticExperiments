"""
Barista example for no reason!
"""

from dotenv import load_dotenv
import os
from crewai import Agent, Task, Crew, LLM

load_dotenv()

llm_openai = LLM(
    model=os.getenv("MODEL"),
    api_key=os.environ.get(os.getenv("OS_API_KEY_VAR")),
    base_url=os.getenv("API_ENDPOINT"),
    api_version=os.getenv("API_VERSION")
)

user_input = input("Enter your coffee order.")

# Agents
agent_order_taker = Agent(
    role="Friendly Barista",
    goal="Take the customer's coffee order",
    backstory="You're a cheerful barista at a cozy café. You love getting orders right.",
    verbose=True,
    allow_delegation=False,
    llm=llm_openai)

agent_coffee_maker = Agent(
    role="Creative Coffee Maker",
    goal="Prepare the drink based on the order",
    backstory="You're a perfectionist barista who makes coffee with flair and love."
              "You also don't want to bore your customer so describe the coffee while"
              "keeping it short in 3 bullets.",
    verbose=True,
    allow_delegation=False,
    llm=llm_openai
)

agent_till_manager = Agent(
    role="Efficient Till Staff",
    goal="Based on the order and applied discount, ask for payment.",
    backstory="You are the most efficient till manager and you always add up the right amount to "
              "charge for customers, like add-on syrup and service tax.",
    verbose=True,
    allow_delegation=False,
    llm=llm_openai
)

# Tasks
task_order_taker = Task(
    description=f"Based on the order here {user_input} repeat and confirm the order with the customer and the date & "
                f"time now",
    agent=agent_order_taker,
    expected_output="Politely repeat the order for confirmation with the date & time"
)

task_coffee_maker = Task(
    description="Based on the order from barista, describe how you would make that coffee drink.",
    agent=agent_coffee_maker,
    context=[task_order_taker],
    expected_output="A coffee description and shout-out"
)

task_till_manager = Task(
    description="A cappuccino costs 3 Euro, latte 3.5, mocha 3.5, any syrup: 50 cents. "
                "Apply discount depending on the day: Thursday 5% off, Friday 20%"
                "Include 2% service tax",
    agent=agent_till_manager,  # I mistakenly added agent_order_taker and it never gave any error plus worked like a charm.
    expected_output="Request the customer for payment with breakdown."
)

# Create Crew
crew = Crew(
    agents=[agent_order_taker, agent_coffee_maker, agent_till_manager],
    tasks=[task_order_taker, task_coffee_maker, task_till_manager],
    # process=Process.sequential
    verbose=True
)

# Get going you robots...
result = crew.kickoff()
# print(result)
