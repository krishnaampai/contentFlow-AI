from crewai import Agent
from config.settings import get_llm

def create_researcher():
    return Agent(
        role="Researcher",
        goal="Find useful information",
        backstory="Expert in research and analysis",
        verbose=True,
        llm=get_llm()  
    )