from crewai import Task

def editing_task(agent, context_tasks):
    return Task(
        description="""Review the copywriter's drafts against the researcher's fact sheet.
        
        Check for:
        1. Hallucinations — any invented features, wrong prices, false claims
        2. Tone issues — too salesy, too robotic, or off-brand
        3. Missing value proposition — is it the hero of each piece?
        
        For each piece (blog, social, email) give: APPROVED or REJECTED + reason.
        If rejected, write a specific correction note.""",
        expected_output="""Quality control report:
        
        BLOG: [APPROVED/REJECTED]
        Reason: ...
        
        SOCIAL THREAD: [APPROVED/REJECTED]  
        Reason: ...
        
        EMAIL: [APPROVED/REJECTED]
        Reason: ...
        
        OVERALL QUALITY SCORE: X/10
        HALLUCINATIONS FOUND: (list or 'None')""",
        agent=agent,
        context=context_tasks
    )