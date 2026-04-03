from crewai import Task

#For testing
MOCK_DATA = """
Product: DataSync Pro 3.0
AI-powered data integration platform.
Features: real-time sync, 200+ connectors, 99.7% accuracy.
Pricing: $299/month for 25 users (was $450).
Target: Mid-market B2B SaaS companies.
Value prop: Cut data engineering costs by 60%, ship 3x faster.
Launch: April 15, 2026. SOC2 certified.
"""

def research_task(agent,  source_text):
    return Task(
        description=f"""Analyze this source material and extract a structured fact sheet:

        Source:
        {source_text}

        Extract: product name, key features, pricing, target audience,
        value proposition, technical specs. Flag any ambiguous statements.""",
        expected_output="""A structured fact sheet in markdown with sections:
        - Product Overview
        - Key Features (bullet list)
        - Pricing
        - Target Audience
        - Value Proposition
        - Ambiguous Statements (if any)""",
        agent=agent
    )