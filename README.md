# My AgenticAI Experiments

This is where I have documented all my agentic AI experiments.
✅ All systems are currently **running fine** as of **August 4, 2025**.

# Set-Up

```bash
cd $your_project
python -m venv crewai_env 
crewai_env\Scripts\activate
python -m pip install -r requirements.txt
```

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

# Starter Code

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

# Extension of the Starter Code

I cooked up a naive experiment for sequential tasks.

Specs:

- Number of Agents: 3
- Number of Tasks: 3
- No delegation
- Relationship: Sequential
- Dependency/Context: Task 2 need the context of Task 1

Python File Link: https://github.com/royn5618/AgenticExperiments/blob/main/CrewAI/1_SimpleExperiments/2_extending_example.py

⚠️ Important: I mistakenly added agent1 to task3 instead of agent3 and it worked like a charm. The agent 3 was never used initially until I tried interpreting the report.











