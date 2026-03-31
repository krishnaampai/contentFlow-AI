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


# ── Section parsing ────────────────────────────────────────────────────────────

_SECTION_PATTERNS = {
    "blog":   r'(?:BLOG(?:\s+POST)?[\s:]+)(.*?)(?=SOCIAL|EMAIL|$)',
    "social": r'(?:SOCIAL(?:\s+(?:THREAD|MEDIA))[\s:]*)(.*?)(?=BLOG|EMAIL|$)',
    "email":  r'(?:EMAIL(?:\s+(?:NEWSLETTER|TEASER))?[\s:]+)(.*?)(?=BLOG|SOCIAL|$)',
}

_REGEN_PATTERNS = {
    "blog":   r'##\s*BLOG\s*POST\s*(.*?)(?=##\s*SOCIAL|##\s*EMAIL|$)',
    "social": r'##\s*SOCIAL\s*THREAD\s*(.*?)(?=##\s*BLOG|##\s*EMAIL|$)',
    "email":  r'##\s*EMAIL\s*TEASER\s*(.*?)(?=##\s*BLOG|##\s*SOCIAL|$)',
}


def parse_content_sections(raw: str) -> tuple:
    """Split full pipeline output into (blog, social, email)."""
    results = {}
    for key, pattern in _SECTION_PATTERNS.items():
        m = re.search(pattern, raw, re.DOTALL | re.IGNORECASE)
        results[key] = m.group(1).strip() if m else ""

    # Fallback: divide by triple newlines
    if not any(results.values()):
        parts = [p.strip() for p in re.split(r'\n{3,}', raw) if p.strip()]
        for i, key in enumerate(["blog", "social", "email"]):
            results[key] = parts[i] if i < len(parts) else ""

    return results["blog"], results["social"], results["email"]


def extract_single_piece(raw: str, content_type: str) -> str:
    """Pull one labelled section from a single-piece regeneration response."""
    m = re.search(_REGEN_PATTERNS[content_type], raw, re.DOTALL | re.IGNORECASE)
    return m.group(1).strip() if m else raw.strip()