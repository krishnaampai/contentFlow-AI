from crewai import Agent
from config.settings import get_llm

def create_editor():
    return Agent(
        role="Editor-in-Chief",
        goal="Review content for accuracy, tone, and quality. Reject anything that contradicts the research.",
        backstory="""You are a strict editor who never lets incorrect or 
        off-brand content pass. You compare every draft against the original 
        research and flag hallucinations, wrong facts, or bad tone.""",
        verbose=True,
        llm=get_llm()
    )