import re
from utils.content import markdown_to_html


# ── Log renderer ───────────────────────────────────────────────────────────────

_LOG_COLORS = {
    "❌": "#ef4444",
    "✅": "#22c55e",
    "🎉": "#22c55e",
    "🔍": "#f59e0b",
    "🧠": "#f59e0b",
    "✍️": "#f59e0b",
    "🚀": "#f59e0b",
    "Agent:": "#38bdf8",
    "Final Answer:": "#38bdf8",
}
_DEFAULT_LOG_COLOR = "#94a3b8"


def render_log_html(logs: list) -> str:
    """Convert a list of log strings into a coloured HTML block."""
    html = ""
    for line in logs:
        color = next(
            (c for symbol, c in _LOG_COLORS.items() if symbol in line),
            _DEFAULT_LOG_COLOR,
        )
        html += (
            f"<p style='color:{color};font-family:monospace;"
            f"margin:2px 0;font-size:13px'>{line}</p>"
        )
    return html


# ── Social mobile preview ──────────────────────────────────────────────────────

def render_social_mobile_preview(content: str) -> str:
    """Render social thread as fake Twitter/X phone frame."""
    tweets = [t.strip() for t in re.split(r'\n\n+|\d+[\./]\s', content) if t.strip()]
    tweets = tweets[:6]

    cards_html = ""
    for i, tw in enumerate(tweets):
        cards_html += f"""
        <div style="background:#1a2332;border:1px solid #2d3f55;border-radius:16px;
                    padding:14px 16px;margin-bottom:10px;">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
            <div style="width:36px;height:36px;border-radius:50%;
                        background:linear-gradient(135deg,#38bdf8,#6366f1);
                        display:flex;align-items:center;justify-content:center;
                        font-size:14px;font-weight:bold;color:#fff;">CF</div>
            <div>
              <div style="color:#e2e8f0;font-weight:600;font-size:13px;">ContentFlow</div>
              <div style="color:#64748b;font-size:11px;">@contentflow_ai</div>
            </div>
            <div style="margin-left:auto;color:#1d9bf0;font-size:18px;">𝕏</div>
          </div>
          <div style="color:#cbd5e1;font-size:13px;line-height:1.6;">{tw}</div>
          <div style="display:flex;gap:20px;margin-top:10px;color:#64748b;font-size:12px;">
            <span>🗨 {12 + i * 3}</span>
            <span>🔁 {5 + i}</span>
            <span>❤️ {34 + i * 7}</span>
          </div>
        </div>"""

    return f"""
    <div style="max-width:375px;margin:0 auto;background:#0f172a;border-radius:24px;
                border:8px solid #1e293b;padding:16px;
                box-shadow:0 0 0 2px #334155,0 20px 60px rgba(0,0,0,0.5);">
      <div style="display:flex;justify-content:center;margin-bottom:12px;">
        <div style="width:80px;height:4px;background:#334155;border-radius:2px;"></div>
      </div>
      <div style="text-align:center;color:#38bdf8;font-size:12px;font-weight:600;
                  letter-spacing:2px;margin-bottom:14px;">TWITTER / X</div>
      {cards_html}
    </div>"""


# ── Blog desktop preview ───────────────────────────────────────────────────────

def render_blog_desktop_preview(content: str) -> str:
    """Render blog post inside a fake browser chrome."""
    html_body = markdown_to_html(content)
    return f"""
    <div style="background:#f8fafc;border-radius:12px;border:1px solid #e2e8f0;
                overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.3);">
      <div style="background:#e2e8f0;padding:10px 14px;display:flex;align-items:center;gap:8px;">
        <div style="width:10px;height:10px;border-radius:50%;background:#ef4444;"></div>
        <div style="width:10px;height:10px;border-radius:50%;background:#f59e0b;"></div>
        <div style="width:10px;height:10px;border-radius:50%;background:#22c55e;"></div>
        <div style="flex:1;background:#fff;border-radius:6px;padding:4px 12px;
                    font-size:11px;color:#64748b;margin:0 16px;">
          contentflow.ai/blog/post
        </div>
      </div>
      <div style="padding:32px 48px;background:#fff;color:#1e293b;
                  font-family:'Georgia',serif;font-size:16px;line-height:1.8;
                  max-height:480px;overflow-y:auto;">
        <div style="max-width:680px;margin:0 auto;">{html_body}</div>
      </div>
    </div>"""


# ── Blog mobile preview ────────────────────────────────────────────────────────

def render_blog_mobile_preview(content: str) -> str:
    """Render blog post inside a fake phone frame."""
    html_body = markdown_to_html(content)
    return f"""
    <div style="max-width:375px;margin:0 auto;background:#0f172a;border-radius:24px;
                border:8px solid #1e293b;padding:12px;
                box-shadow:0 0 0 2px #334155,0 20px 60px rgba(0,0,0,0.5);">
      <div style="display:flex;justify-content:center;margin-bottom:8px;">
        <div style="width:80px;height:4px;background:#334155;border-radius:2px;"></div>
      </div>
      <div style="background:#fff;border-radius:14px;padding:16px;color:#1e293b;
                  font-family:Georgia,serif;font-size:13px;line-height:1.7;
                  max-height:500px;overflow-y:auto;">
        {html_body}
      </div>
    </div>"""


# ── CSS theme ──────────────────────────────────────────────────────────────────

APP_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

.stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 60%, #0f172a 100%); color: #e2e8f0; }
h1, h2, h3 { color: #38bdf8; font-family: 'Space Mono', monospace; }
p, li, label { font-family: 'DM Sans', sans-serif; }

.card {
    background: rgba(30, 41, 59, 0.7);
    backdrop-filter: blur(12px);
    border-radius: 20px;
    padding: 24px;
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 16px;
}
.content-card {
    background: rgba(15, 23, 42, 0.8);
    border-radius: 16px;
    padding: 20px;
    border: 1px solid rgba(56, 189, 248, 0.15);
    margin-bottom: 8px;
}
.accepted-badge {
    display: inline-block;
    background: rgba(34, 197, 94, 0.15);
    color: #22c55e;
    border: 1px solid rgba(34, 197, 94, 0.3);
    border-radius: 20px;
    padding: 2px 12px;
    font-size: 12px;
    font-weight: 600;
    margin-left: 10px;
    font-family: 'DM Sans', sans-serif;
}
.section-header { display: flex; align-items: center; margin-bottom: 16px; }

div[data-testid="stButton"] > button {
    font-family: 'DM Sans', sans-serif;
    border-radius: 10px;
    border: none;
    font-weight: 500;
    transition: all 0.2s ease;
}
.stTabs [data-baseweb="tab"] { font-family: 'DM Sans', sans-serif; color: #94a3b8; }
.stTabs [aria-selected="true"] { color: #38bdf8 !important; }
</style>
"""