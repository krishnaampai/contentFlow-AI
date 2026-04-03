import re


#  Markdown 

def decode_markdown(text: str) -> str:
    """Strip markdown to plain text (used for log cleaning)."""
    text = re.sub(r'#{1,6}\s*', '', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'```[a-z]*', '', text)
    text = re.sub(r'```', '', text)
    return text.strip()


def markdown_to_html(text: str) -> str:
    """Convert markdown to basic HTML for st.markdown rendering."""
    text = re.sub(r'^### (.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.+)$',  r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.+)$',   r'<h1>\1</h1>', text, flags=re.MULTILINE)
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.*?)\*',     r'<em>\1</em>', text)
    text = re.sub(r'^\* (.+)$', r'<li>\1</li>', text, flags=re.MULTILINE)
    text = re.sub(r'^- (.+)$',  r'<li>\1</li>', text, flags=re.MULTILINE)
    text = re.sub(
        r'(<li>.*?</li>\n?)+',
        lambda m: '<ul>' + m.group(0) + '</ul>',
        text, flags=re.DOTALL,
    )
    text = re.sub(r'\n\n+', '<br><br>', text)
    text = re.sub(r'\n', '<br>', text)
    return text



