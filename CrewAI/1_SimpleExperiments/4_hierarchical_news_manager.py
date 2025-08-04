"""
Hierarchical Example:

NewsManager (Manager):
1. News Analyst: Gets incoming news and assess whereabouts like date & location, location, reporter, category of news
2. Report Writer: Based on the news report analysis and the original text creates a markdown report in a given format
3. Tele Script-writer: Based on the report, generates a script for the television journalist
4. Content Reviewer: Based on the Report and Summary, generates a full story with headlines & a given format to publish
"""

from dotenv import load_dotenv
import os
from crewai import Agent, Task, Crew, LLM, Process

load_dotenv()

# This is an LLM that sticks to facts
llm_openai_factual = LLM(
    model=os.getenv("MODEL"),
    api_key=os.environ.get(os.getenv("OS_API_KEY_VAR")),
    base_url=os.getenv("API_ENDPOINT"),
    api_version=os.getenv("API_VERSION"),
    temperature=1
)

# This is an LLM that has some freedom, for the reporter to be creative but also factual
# Dunno will they ever fight for lower temperature!?
# See I couldn't name this cractual if I were temperature 1
# I need to be temperature (almost) zero to write something like that --- Ignore ME!
llm_openai_cractual = LLM(
    model=os.getenv("MODEL"),
    api_key=os.environ.get(os.getenv("OS_API_KEY_VAR")),
    base_url=os.getenv("API_ENDPOINT"),
    api_version=os.getenv("API_VERSION"),
    temperature=0.8
)

# This is for the LLM to be creative when re-writing facts for the news website and the news channel
llm_openai_creative = LLM(
    model=os.getenv("MODEL"),
    api_key=os.environ.get(os.getenv("OS_API_KEY_VAR")),
    base_url=os.getenv("API_ENDPOINT"),
    api_version=os.getenv("API_VERSION"),
    temperature=0.6
)

user_input = input("Enter the news from field: \n")

# -------------- MANAGER AGENT BEGIN --------------- #
agent_news_manager = Agent(
    role="News Manager",
    goal="Managing and orchestrating a team of specialized AI agents. "
         "Your ONLY role is to manage the workflow by activating the appropriate agent at the appropriate time. "
         "You are NOT responsible for evaluating the quality or content of any agent's work.",
    backstory="""You are the News Manager, an AI coordinator responsible for orchestrating a team of specialized 
    AI agents. Your ONLY role is to manage the workflow by activating the appropriate agent at the appropriate time. 
    You are NOT responsible for evaluating the quality or content of any agent's work.
    
    ## WORKFLOW COORDINATION RESPONSIBILITIES
    
    1. **Start with News Analyst as coworker**:
        - Always begin the workflow by activating the News Analyst
        - The News Analyst will create a extract key metadata from the incoming raw news from on-field journalist
        - After the News Analyst completes the work, activate the News Report Writer
    
    2. **Activate News Report Writer as coworker**:
        - After the News Analyst has finished, activate the News Report Writer
        - Provide the News Report Writer with the metadata extracted by the News Analyst and the original script
        - The News Report Writer will write a comprehensive news fit to publish on website
        - After the News Report Writer completes the work, activate the Script Writer for Television Journalists
    
    3. **Activate Script Writer for Television Journalists as coworker**:
        - After the News Report Writer has finished, activate the Script Writer for Television Journalists
        - The Script Writer for Television Journalists will write a script for the on-air television journalist
        - After the Script Writer for Television Journalists completes the work, activate the Content Reviewer
    
    4. **Activate Content Reviewer as coworker**:
        - After the Script Writer for Television Journalists has finished, activate the Content Reviewer
        - The Content Reviewer reviews the content produced by News Report Writer and Script Writer for Television Journalists
        - The Content Reviewer first reviews the Website Article written by the News Report Writer and provides a decision and a reason.
        - After the Content Reviewer completes reviewing the tele-script written by the Script Writer for Television Journalists and provides a decision and a reason.
        - This the last action and DO NOT ACTIVATE any other agent.
    """,
    llm=llm_openai_factual,
    allow_delegation=True,
    verbose=True,
)

# -------------- MANAGER AGENT COMPLETE@ --------------- #

# -------------- AGENTS BEGIN --------------- #
agent_news_analyser = Agent(
    role="News Analyst",
    goal="Analyse the incoming news to assess the metadata like date & location, location, "
         "veracity, reporter name, category of news.",
    backstory="""You are a news analyst. You should read the news transcript 
    send by the on field news reported and use the following format to fill up:
     1. Reporter Name: <reporter name>
     2. Location of Incident: <location where the incident has happened / is happening
     3. Fake News: Options - Yes, No, May Be
     4. Reason: <Provide reason for thinking this is potentially a fake news.
     5. News Category: Options - International, Economy, Political, Sports, Tourism, Others
     6. Breaking News: Options - Yes or No 
      """,
    verbose=True,
    allow_delegation=False,
    llm=llm_openai_factual)  # LLM needs to stick to facts

agent_report_writer = Agent(
    role="News Report Writer",
    goal="Prepare a report of the news based on the news analysed by the analyst.",
    backstory="""You are a News Report Writer who keeps the tone professional and used the facts to create 
    news script for the website. Use the original story and write the story in the following format:
    ---
    [NEWS TITLE] - in under 8 words
    [DATE], [TIME], [LOCATION]: 
    [NEWS SUMMARY] - in 3 bullets
    
    Full Report:
    [INTRODUCTION] - Upto 3 lines in 1 paragraph
    [BODY] - Upto 3 paragraphs
    [CONCLUSION] - Upto 3 lines in 1 paragraph
    News Reported By [REPORTER NAME]
    ---
    """,
    verbose=True,
    allow_delegation=False,
    llm=llm_openai_cractual  # This one can be a bit creative
)

agent_tele_script_writer = Agent(
    role="Script Writer for Television Journalists",
    goal="Based on the full report generated by the Report Writer and the News Analyst, write a tele script.",
    backstory=""""
    You are a script writer for the on-air television journalist who will read it out for the viewers of the channel.
    Here are a few rules:
    1. It is mandatory to mention if the news is a potential fake news.
    2. You are not supposed to take sides.
    3. Be factual, professional but include a good hook line for opening the news.
    4. Optional: Use one or two comical references for the news, depending on how serious it is. 
    """,
    verbose=True,
    allow_delegation=False,
    llm=llm_openai_creative
)

agent_content_reviewer = Agent(
    role="Content Reviewer",
    goal="Read the given content and make sure if everything looks perfect. Make necessary changes if needed.",
    backstory="""You are an efficient content reviewer. You will review either the tele script or the article for the
    website with utmost sincerity that no false or misleading information is relayed. You should either 
    approve it or reject it, stating a proper reason.""",
    verbose=True,
    allow_delegation=False,
    llm=llm_openai_cractual
)

# -------------- AGENTS COMPLETED --------------- #

# -------------- TASKS BEGIN --------------- #
task_analyse_news = Task(
    description=f"Based on the on-fielder news reported here {user_input} extract metadata.",
    agent=agent_news_analyser,
    expected_output="""A good markdown format plan.
        IMPORTANT: DO NOT USE ANY MARKDOWN CODE BLOCK SYNTAX (```). 
        The content should be pure markdown without being wrapped in code blocks.
        If you find yourself wanting to wrap the content in ```markdown ... ```, DO NOT DO IT. 
        The content should be directly written in markdown format."""
)

task_create_report = Task(
    description=f"Use the given context and write the news report fit for publishing on website. "
                f"Use the original script: {user_input}",
    agent=agent_report_writer,
    context=[task_analyse_news],
    expected_output="""A good markdown format plan.
        IMPORTANT: DO NOT USE ANY MARKDOWN CODE BLOCK SYNTAX (```). 
        The content should be pure markdown without being wrapped in code blocks.
        If you find yourself wanting to wrap the content in ```markdown ... ```, DO NOT DO IT. 
        The content should be directly written in markdown format."""
)

task_write_tele_script = Task(
    description="Write a script based on the news for the on-air television journalist. ",
    agent=agent_tele_script_writer,
    expected_output="""A good markdown format plan.
            IMPORTANT: DO NOT USE ANY MARKDOWN CODE BLOCK SYNTAX (```). 
            The content should be pure markdown without being wrapped in code blocks.
            If you find yourself wanting to wrap the content in ```markdown ... ```, DO NOT DO IT. 
            The content should be directly written in markdown format."""
)

task_review_content = Task(
    description="Review the content provided for publishing on website and the tele-script for on-air journalist. ",
    agent=agent_content_reviewer,
    context=[task_create_report, task_write_tele_script],
    expected_output="""Answer in the following format:
    ---
    # Website Article
    ## Status: <Approved or Rejected>
    ## Reason: <Write the reason in bullets>
    ## Full Article:
    
    # TeleScript
    ## Status: <Approved or Rejected>
    ## Reason: <Write the reason in bullets>
    ## Full Script:
    ---
    """
)

# -------------- TASKS COMPLETED --------------- #

# Create Crew
crew = Crew(
    agents=[agent_news_analyser, agent_report_writer, agent_tele_script_writer,
            agent_content_reviewer],
    tasks=[task_analyse_news, task_create_report, task_write_tele_script, task_review_content],
    process=Process.hierarchical,
    # planning=True,  # If any planning is required.
    planning_llm=llm_openai_factual,  # If planning is required and done by LLM, use this
    manager_agent=agent_news_manager,  # I have a manager agent explicitly configured, so I set this param
    # manager_llm = None,  # If management is done by LLM, set this one up.
    verbose=True
)

# Get going you robots...
result = crew.kickoff()
print('------------------------RESULT---------------------------------- ')
print(result)
