"""
Example From: https://docs.crewai.com/en/learn/custom-manager-agent
"""

from dotenv import load_dotenv
import os
from crewai import Agent, Task, Crew, Process, LLM

load_dotenv()

# This is an LLM that sticks to facts
llm_openai = LLM(
    model=os.getenv("MODEL"),
    api_key=os.environ.get(os.getenv("OS_API_KEY_VAR")),
    base_url=os.getenv("API_ENDPOINT"),
    api_version=os.getenv("API_VERSION"),
    temperature=1
)

# Define your agents
researcher = Agent(
    role="Researcher",
    goal="Conduct thorough research and analysis on AI and AI agents",
    backstory="You're an expert researcher, specialized in technology, software engineering, AI, and startups. You "
              "work as a freelancer and are currently researching for a new client.",
    allow_delegation=False,
    llm=llm_openai
)

editor = Agent(
    role="Senior Writer/Editor",
    goal="Create and Edit compelling content about AI and AI agents",
    backstory="You're a senior writer/editor, specialized in technology, software engineering, AI, and startups. "
              "You work as a freelancer and are currently writing and editing content for a new client.",
    allow_delegation=False,
    llm=llm_openai
)

# Define your task
task = Task(
    description="Generate a list of 5 interesting ideas for an article, then write one captivating "
                "paragraph for each idea that showcases the potential of a full article on this topic. "
                "Return the list of ideas with their paragraphs and your notes.",
    expected_output="5 bullet points, each with a paragraph and accompanying notes.",
)

# Original Manager Agent
og_manager = Agent(
    role="Project Manager",
    goal="Efficiently manage the crew and ensure high-quality task completion",
    backstory="You're an experienced project manager, skilled in overseeing complex projects "
              "and guiding teams to success. Your role is to coordinate the efforts of the crew "
              "members, ensuring that each task is completed on time and to the highest standard.",
    allow_delegation=True,
)


# Edited the manager agent
new_manager = Agent(
    role="Project Manager",
    goal="Efficiently manage the crew and ensure high-quality task completion",
    backstory="You're an experienced project manager, skilled in overseeing complex "
              "projects and guiding teams to success. Your role is to coordinate the "
              "efforts of the crew members, ensuring that each task is completed on time "
              "and edited to the highest standard.",
    allow_delegation=True,
    llm=llm_openai
)

# Instantiate your crew with a custom manager
crew = Crew(
    agents=[researcher, editor],
    tasks=[task],
    manager_agent=new_manager, # Try og_manager to understand the different between thoughts and task delegation
    process=Process.hierarchical,
    verbose=True
)

# Start the crew's work
result = crew.kickoff()
print('------------------------RESULT---------------------------------- ')
print(result)
