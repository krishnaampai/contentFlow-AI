from crewai import Agent
from config.settings import get_llm

def create_writer():
    return Agent(
        role="Creative Copywriter",
        goal="Transform research into compelling multi-format marketing content",
        backstory="""You are a skilled copywriter who specializes in turning 
        technical research into engaging content. You write blog posts, 
        social media threads, and email teasers with distinct tones for each.""",
        verbose=True,
        llm=get_llm()
    )