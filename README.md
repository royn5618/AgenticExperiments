# My AgenticAI Experiments

This is where I have documented all my agentic AI experiments.

✅ All systems are currently **running fine** as of **August 4, 2025**.
---
# Set-Up

```bash
cd $your_project
python -m venv crewai_env 
crewai_env\Scripts\activate
python -m pip install -r requirements.txt
```
---
# LLM Set-Up
Note: I am using Azure OpenAI Deployment using this code here:

```python
llm_openai = LLM(
    model=os.getenv("MODEL"),
    api_key=os.environ.get(os.getenv("OS_API_KEY_VAR")),
    base_url=os.getenv("API_ENDPOINT"),
    api_version=os.getenv("API_VERSION")
)
```
You can also set the parameters for LLMs like temperatue etc here.
---
# Experiment 1: Starter Code

I have used a simple example borrowed from the linked tutorial. 

Specs:

- Number of Agents: 2
- Number of Tasks: 2
- No delegation
- Relationship: Sequential
- Dependency/Context: Task 2 need the context of Task 1
  
Links:
- Reference Video: https://www.youtube.com/watch?v=6NbJQsCg1VQ&t=249s
- Reference Git: https://github.com/leonvanzyl/crewai-youtube/blob/master/main.py
- Python File Link: https://github.com/royn5618/AgenticExperiments/blob/main/CrewAI/1_SimpleExperiments/1_crew_ai_exp.py
---
# Experiment 2: Extension of the Starter Code

I cooked up a naive experiment for **sequential** tasks.

Specs:

- Number of Agents: 3
- Number of Tasks: 3
- No delegation
- Relationship: Sequential
- Dependency/Context: Task 2 need the context of Task 1

Link:
- Python File Link: https://github.com/royn5618/AgenticExperiments/blob/main/CrewAI/1_SimpleExperiments/2_extending_example.py
- Output PDF Link: https://github.com/royn5618/AgenticExperiments/blob/main/CrewAI/1_SimpleExperiments/2_Output.pdf

⚠️ Important: I mistakenly added agent1 to task3 instead of agent3 and it worked like a charm. The agent 3 was never used initially until I tried interpreting the report.
---
# Experiment 3: Using Decorators

Once I got a hang of this sequential process, I thought it is time to look at the **yaml files and decorators**. So I transferred the same example of **Barista** to this format.

I built my first agentic class: **LePetitCafeCrew** with the same configuration at above.

Links:
- Config files with yaml files of agents and tasks: https://github.com/royn5618/AgenticExperiments/tree/main/CrewAI/2_DecoratorExample/Barista/config
- Main (where the crew resides): https://github.com/royn5618/AgenticExperiments/blob/main/CrewAI/2_DecoratorExample/Barista/main.py
---
# Experiment 4: Using Hierarchical Process

So this is where it got easy at first and then confusing. Let's dive into the easy part where I copied the code directly from CrewAI's docs for understanding how it works:

Specs:

- Number of Manager Agent: 1
- Number of Agents: 2
- Number of Tasks: 1
- Degation by Manager Agent
- Relationship: Hierarchical
- Dependency/Context: There is no context given. The manager delegates the tasks based on its role, goal and backstory.

⚠️ Important: I did use the original backstory provided by CrewAI but it did not work. It wasn't engaging the writer agent at all. So I modified the backstory and ran the script again to find that the agent is correctly delegating the work. 

**Manager Configs:**

```python
# Original Manager
og_manager = Agent(
    role="Project Manager",
    goal="Efficiently manage the crew and ensure high-quality task completion",
    backstory="You're an experienced project manager, skilled in overseeing complex projects "
              "and guiding teams to success. Your role is to coordinate the efforts of the crew "
              "members, ensuring that each task is completed on time and to the highest standard.",
    allow_delegation=True,
)

# NEW Manager
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
```

Here's the difference between the settings of the managers:

**OG Manager**
- ✅ Delegation enabled
- ❌ No LLM attached
- 🧠 Behavior:
    - uses default built-in planning logic
    - Very basic task routing
    - No deep understanding of task details
    - Can delegate, but lacks context-rich thinking

**NEW Manager**
- ✅ Delegation enabled
- ✅ LLM attached
- 🧠 Behavior:
    - can analyze, restructure, and assign tasks intelligently
    - Uses the task description and agents’ roles to plan a smart hierarchy
    - Can write new instructions, provide feedback, and restructure work based on results
---
# Experiment 5: News Manager

Okay! So it got complicated.. haha... and I may have made it complicated.

So here's the deal and below is what I wanted:

**NewsManager (Manager Agent):**
1. News Analyst: Gets incoming news and assess whereabouts like date & location, location, reporter, category of news
2. Report Writer: Based on the news report analysis and the original text creates a markdown report in a given format
3. Tele Script-writer: Based on the report, generates a script for the television journalist
4. Content Reviewer: Based on the Report and Summary, generates a full story with headlines & a given format to publish

And it went on spiralling with a lot issues since I started experimenting vehemently with reusing tasks, multiple tasks to multiple agents and agents delegating using different backstories and description.... phew!

In the end it all got together ... BUT ... I used different LLM settings.

```python
# For Extracting Metadata and planning
llm_openai_factual = LLM(
    model=os.getenv("MODEL"),
    api_key=os.environ.get(os.getenv("OS_API_KEY_VAR")),
    base_url=os.getenv("API_ENDPOINT"),
    api_version=os.getenv("API_VERSION"),
    temperature=1
)

# This is an LLM that has some freedom, for the reporter to be creative but also factual - cractual!
llm_openai_cractual = LLM(
    model=os.getenv("MODEL"),
    api_key=os.environ.get(os.getenv("OS_API_KEY_VAR")),
    base_url=os.getenv("API_ENDPOINT"),
    api_version=os.getenv("API_VERSION"),
    temperature=0.8
)

# This is for the LLM to be creative when re-writing facts for the news channel broadcast
llm_openai_creative = LLM(
    model=os.getenv("MODEL"),
    api_key=os.environ.get(os.getenv("OS_API_KEY_VAR")),
    base_url=os.getenv("API_ENDPOINT"),
    api_version=os.getenv("API_VERSION"),
    temperature=0.6
)
```

The news manager currently identifies the need to have an analyst extract metadata, then use the report write to write the article in the given format, then use the tele script writer to create a script that the on-air television journalist can use and finally, uses the content reviewer to approve or reject with appropriate comments for both - the article and the script.
---

*That's all folks for now! Will come back with using tools, agno and nested crews soon*

