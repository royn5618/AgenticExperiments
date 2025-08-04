"""
Reference Video: https://www.youtube.com/watch?v=6NbJQsCg1VQ&t=249s
Reference Git: https://github.com/leonvanzyl/crewai-youtube/blob/master/main.py
"""
from dotenv import load_dotenv
import os
from crewai import Agent, Task, Crew, LLM
# from openai import AzureOpenAI

load_dotenv()

# --- NOT USING - CONNECTION BLOCKED ---
# The DuckDuckGo tool allows AI agents to:
# - Perform real-time internet searches
# - Retrieve up-to-date information
# - Answer questions that require current or external knowledge
# search_tool = DuckDuckGoSearchRun()

llm_openai = LLM(
    model=os.getenv("MODEL"),
    api_key=os.environ.get(os.getenv("OS_API_KEY_VAR")),
    base_url=os.getenv("API_ENDPOINT"),
    api_version=os.getenv("API_VERSION")
)

# Team Member
researcher = Agent(
    role='Senior Research Analyst',
    goal='Uncover cutting-edge developments in AI & Data Science',
    backstory="""You work at a leading tech think tank.
    Your expertise lies in identifying emerging trends.
    You have a knack for dissecting complex data and presenting
    actionable insights.""",
    verbose=True,
    allow_delegation=False,
    llm=llm_openai)
# tools=[search_tool]

writer = Agent(
    role='Tech Content Strategist',
    goal='Craft compelling content on tech advancements',
    backstory="""You are a renowned Content Strategist, known for
  your insightful and engaging articles.
  You transform complex concepts into compelling narratives.""",
    verbose=True,
    allow_delegation=False,
    llm=llm_openai
)

# Tasks
task_researcher = Task(
    description="""Conduct a comprehensive analysis of the latest advancements in AI in 2024.
    Identify key trends, breakthrough technologies, and potential industry impacts.
    Your final answer MUST be a full analysis report""",
    agent=researcher,
    expected_output="Generate a summary report"
)

task_writer = Task(
    description="""Using the insights provided, develop an engaging blog
    post that highlights the most significant AI advancements.
    Your post should be informative yet accessible, catering to a tech-savvy audience.
    Make it sound cool, avoid complex words so it doesn't sound like AI.
    Your final answer MUST be the full blog post of at least 4 paragraphs.""",
    agent=writer,
    context=[task_researcher],
    expected_output="Your final answer MUST be the full blog post of at least 4 paragraphs."
)

# Create Crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[task_researcher, task_writer],
    # process=Process.sequential
    verbose=True
)

# Get going you robots...
result = crew.kickoff()

print(result)
