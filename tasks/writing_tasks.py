from crewai import Task

def writing_task(agent, context_tasks):
    return Task(
        description="""Using ONLY the facts from the researcher's fact sheet, create:
        
        1. A 400-500 word blog post (tone: professional, trustworthy)
        2. A 5-post social media thread (tone: punchy, engaging)
        3. A 1-paragraph email teaser (tone: personalized, exciting)
        
        The value proposition must be the hero of every piece.
        Do NOT invent features or prices not in the fact sheet.""",
        expected_output="""Three content pieces clearly labeled:
        ## BLOG POST
        (content here)
        
        ## SOCIAL THREAD
        Post 1: ...
        Post 2: ...
        Post 3: ...
        Post 4: ...
        Post 5: ...
        
        ## EMAIL TEASER
        (content here)""",
        agent=agent,
        context=context_tasks
    )

def rewrite_task(agent, correction_note, context_tasks):
    return Task(
        description=f"""The Editor-in-Chief has reviewed your drafts and sent back corrections.
        
        CORRECTION NOTE FROM EDITOR:
        {correction_note}
        
        Fix ONLY what the editor flagged. Do not change approved sections.
        Use ONLY facts from the researcher's fact sheet — no new inventions.""",
        expected_output="""The corrected content pieces, clearly labeled:
        ## BLOG POST
        (content here)
        
        ## SOCIAL THREAD
        Post 1: ...
        Post 2: ...
        Post 3: ...
        Post 4: ...
        Post 5: ...
        
        ## EMAIL TEASER
        (content here)""",
        agent=agent,
        context=context_tasks
    )