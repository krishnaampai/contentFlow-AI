import re
import io
import time
import queue
import zipfile
import threading
import streamlit as st
from crew.crew import run_pipeline ,regenerate_piece

# ---------- Page Config ----------
st.set_page_config(page_title="ContentFlow AI", layout="wide")

# ---------- Session State ----------
defaults = {
    "result": None,
    "review": None,
    "logs": [],
    "running": False,
    "source_text_snapshot": "",
    # Parsed content pieces
    "blog_content": "",
    "social_content": "",
    "email_content": "",
    # Accepted flags
    "blog_accepted": False,
    "social_accepted": False,
    "email_accepted": False,
    # Regenerating flags
    "blog_regen": False,
    "social_regen": False,
    "email_regen": False,
    # Preview mode per content
    "social_preview_mobile": True,
    "blog_preview_mobile": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------- Log queue ----------
log_queue = queue.Queue()

# ---------- Helpers ----------
def should_show_log(msg):
    skip_phrases = [
        "Update Available", "Current version", "Latest version", "uv sync",
        "Crew Execution Started", "Crew Execution Completed", "Tracing Status",
        "Tracing is disabled", "CREWAI_TRACING", "crewai traces",
        "Task Started", "Task Completed", "Task Completion",
        "Crew Completion", "ScriptRunContext",
        "╭─", "╰─", "│", "─╮", "─╯",
        "Name: crew", "ID:", "Final Output:",
        "To enable tracing", "Set tracing=True", "Set CREWAI_TRACING",
        "A new version", "To update, run", "Crew Execution",
    ]
    stripped = msg.strip()
    if not stripped:
        return False
    for phrase in skip_phrases:
        if phrase in stripped:
            return False
    return True

def decode_markdown(text):
    text = re.sub(r'#{1,6}\s*', '', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'```[a-z]*', '', text)
    text = re.sub(r'```', '', text)
    return text.strip()

def markdown_to_html(text):
    text = re.sub(r'^### (.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.+)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.+)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    text = re.sub(r'^\* (.+)$', r'<li>\1</li>', text, flags=re.MULTILINE)
    text = re.sub(r'^- (.+)$', r'<li>\1</li>', text, flags=re.MULTILINE)
    text = re.sub(r'(<li>.*?</li>\n?)+', lambda m: '<ul>' + m.group(0) + '</ul>', text, flags=re.DOTALL)
    text = re.sub(r'\n\n+', '<br><br>', text)
    text = re.sub(r'\n', '<br>', text)
    return text

def add_log(msg):
    clean = decode_markdown(msg)
    if should_show_log(clean):
        log_queue.put(clean)

def render_log_html(logs):
    log_html = ""
    for log in logs:
        if "❌" in log:
            color = "#ef4444"
        elif "✅" in log or "🎉" in log:
            color = "#22c55e"
        elif "🔍" in log or "🧠" in log or "✍️" in log or "🚀" in log:
            color = "#f59e0b"
        elif "Agent:" in log or "Final Answer:" in log:
            color = "#38bdf8"
        else:
            color = "#94a3b8"
        log_html += f"<p style='color:{color}; font-family:monospace; margin:2px 0; font-size:13px'>{log}</p>"
    return log_html

def parse_content_sections(raw_text):
    """
    Parse raw pipeline output into blog, social, and email sections.
    Tries multiple marker patterns for robustness.
    """
    blog, social, email = "", "", ""

    # Pattern 1: labeled sections with colon headers
    patterns = [
        # BLOG POST / BLOG:
        (r'(?:BLOG(?:\s+POST)?[\s:]+)(.*?)(?=SOCIAL|EMAIL|$)', re.DOTALL | re.IGNORECASE),
        # SOCIAL THREAD / SOCIAL MEDIA
        (r'(?:SOCIAL(?:\s+(?:THREAD|MEDIA))[\s:]*)(.*?)(?=BLOG|EMAIL|$)', re.DOTALL | re.IGNORECASE),
        # EMAIL NEWSLETTER / EMAIL:
        (r'(?:EMAIL(?:\s+NEWSLETTER)?[\s:]+)(.*?)(?=BLOG|SOCIAL|$)', re.DOTALL | re.IGNORECASE),
    ]

    blog_match = re.search(patterns[0][0], raw_text, patterns[0][1])
    social_match = re.search(patterns[1][0], raw_text, patterns[1][1])
    email_match = re.search(patterns[2][0], raw_text, patterns[2][1])

    if blog_match:
        blog = blog_match.group(1).strip()
    if social_match:
        social = social_match.group(1).strip()
    if email_match:
        email = email_match.group(1).strip()

    # Fallback: split by double newlines into thirds if nothing parsed
    if not blog and not social and not email:
        parts = [p.strip() for p in re.split(r'\n{3,}', raw_text) if p.strip()]
        if len(parts) >= 3:
            blog, social, email = parts[0], parts[1], parts[2]
        elif len(parts) == 2:
            blog, social = parts[0], parts[1]
        elif len(parts) == 1:
            blog = parts[0]

    return blog, social, email

def run_pipeline_threaded(source_text, result_holder, local_logs_ref):
    """Run pipeline in thread and populate result_holder."""
    try:
        fc, fr = run_pipeline(source_text, log_callback=add_log)
        result_holder["content"] = fc
        result_holder["review"] = fr
    except Exception as e:
        result_holder["error"] = str(e)

def drain_queue_to_list(target_list):
    while not log_queue.empty():
        target_list.append(log_queue.get())

def build_zip(blog, social, email):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        if blog:
            zf.writestr("blog_post.txt", blog)
        if social:
            zf.writestr("social_thread.txt", social)
        if email:
            zf.writestr("email_newsletter.txt", email)
    buf.seek(0)
    return buf.read()

# ---------- Social Mobile Preview ----------
def render_social_mobile_preview(content):
    tweets = [t.strip() for t in re.split(r'\n\n+|\d+[\./]\s', content) if t.strip()]
    tweets = tweets[:6]  # cap at 6 cards
    cards_html = ""
    for i, tw in enumerate(tweets):
        cards_html += f"""
        <div style="background:#1a2332;border:1px solid #2d3f55;border-radius:16px;padding:14px 16px;margin-bottom:10px;">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
            <div style="width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,#38bdf8,#6366f1);display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:bold;color:#fff;">CF</div>
            <div>
              <div style="color:#e2e8f0;font-weight:600;font-size:13px;">ContentFlow</div>
              <div style="color:#64748b;font-size:11px;">@contentflow_ai</div>
            </div>
            <div style="margin-left:auto;color:#1d9bf0;font-size:18px;">𝕏</div>
          </div>
          <div style="color:#cbd5e1;font-size:13px;line-height:1.6;">{tw}</div>
          <div style="display:flex;gap:20px;margin-top:10px;color:#64748b;font-size:12px;">
            <span>🗨 {12+i*3}</span><span>🔁 {5+i}</span><span>❤️ {34+i*7}</span>
          </div>
        </div>"""
    return f"""
    <div style="max-width:375px;margin:0 auto;background:#0f172a;border-radius:24px;border:8px solid #1e293b;padding:16px;
                box-shadow:0 0 0 2px #334155,0 20px 60px rgba(0,0,0,0.5);">
      <div style="display:flex;justify-content:center;margin-bottom:12px;">
        <div style="width:80px;height:4px;background:#334155;border-radius:2px;"></div>
      </div>
      <div style="text-align:center;color:#38bdf8;font-size:12px;font-weight:600;letter-spacing:2px;margin-bottom:14px;">TWITTER / X</div>
      {cards_html}
    </div>"""

# ---------- Blog Desktop Preview ----------
def render_blog_desktop_preview(content):
    html_body = markdown_to_html(content)
    return f"""
    <div style="background:#f8fafc;border-radius:12px;border:1px solid #e2e8f0;overflow:hidden;
                box-shadow:0 4px 24px rgba(0,0,0,0.3);">
      <!-- Browser chrome -->
      <div style="background:#e2e8f0;padding:10px 14px;display:flex;align-items:center;gap:8px;">
        <div style="width:10px;height:10px;border-radius:50%;background:#ef4444;"></div>
        <div style="width:10px;height:10px;border-radius:50%;background:#f59e0b;"></div>
        <div style="width:10px;height:10px;border-radius:50%;background:#22c55e;"></div>
        <div style="flex:1;background:#fff;border-radius:6px;padding:4px 12px;font-size:11px;color:#64748b;margin:0 16px;">
          contentflow.ai/blog/post
        </div>
      </div>
      <!-- Content -->
      <div style="padding:32px 48px;background:#fff;color:#1e293b;font-family:'Georgia',serif;
                  font-size:16px;line-height:1.8;max-height:480px;overflow-y:auto;">
        <div style="max-width:680px;margin:0 auto;">
          {html_body}
        </div>
      </div>
    </div>"""

# ---------- Mobile Blog Preview ----------
def render_blog_mobile_preview(content):
    html_body = markdown_to_html(content)
    return f"""
    <div style="max-width:375px;margin:0 auto;background:#0f172a;border-radius:24px;border:8px solid #1e293b;padding:12px;
                box-shadow:0 0 0 2px #334155,0 20px 60px rgba(0,0,0,0.5);">
      <div style="display:flex;justify-content:center;margin-bottom:8px;">
        <div style="width:80px;height:4px;background:#334155;border-radius:2px;"></div>
      </div>
      <div style="background:#fff;border-radius:14px;padding:16px;color:#1e293b;font-family:Georgia,serif;
                  font-size:13px;line-height:1.7;max-height:500px;overflow-y:auto;">
        {html_body}
      </div>
    </div>"""

# ---------- Custom Theme ----------
st.markdown("""
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

.section-header {
    display: flex;
    align-items: center;
    margin-bottom: 16px;
}

.preview-toggle {
    background: rgba(30,41,59,0.9);
    border: 1px solid rgba(56,189,248,0.2);
    border-radius: 10px;
    padding: 6px;
    display: inline-flex;
    gap: 4px;
    margin-bottom: 16px;
}

/* Streamlit button overrides */
div[data-testid="stButton"] > button {
    font-family: 'DM Sans', sans-serif;
    border-radius: 10px;
    border: none;
    font-weight: 500;
    transition: all 0.2s ease;
}

.stTabs [data-baseweb="tab"] {
    font-family: 'DM Sans', sans-serif;
    color: #94a3b8;
}
.stTabs [aria-selected="true"] {
    color: #38bdf8 !important;
}
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown("""
<div style="text-align:center;padding:20px 0 10px;">
    <h1 style="font-size:2.4rem;margin-bottom:4px;">⚡ ContentFlow AI</h1>
    <p style="color:#64748b;font-family:'DM Sans',sans-serif;font-size:1rem;margin:0;">
        Multi-Agent Content Factory — Generate · Review · Export
    </p>
</div>
""", unsafe_allow_html=True)
st.markdown("---")

# ---------- Input ----------
source_text = st.text_area("📄 Paste Source Content", height=180,
                            placeholder="Paste your article, brief, or notes here…")

# ---------- Launch ----------
if st.button("🚀 Launch Pipeline", use_container_width=True, type="primary"):
    if not source_text.strip():
        st.warning("Please enter source content.")
    else:
        # Reset everything
        for key in ["result", "review", "blog_content", "social_content", "email_content",
                    "blog_accepted", "social_accepted", "email_accepted",
                    "blog_regen", "social_regen", "email_regen", "logs"]:
            st.session_state[key] = defaults[key]
        st.session_state.source_text_snapshot = source_text
        st.session_state.running = True

        while not log_queue.empty():
            log_queue.get()

        local_logs = []
        result_holder = {}

        t = threading.Thread(
            target=run_pipeline_threaded,
            args=(source_text, result_holder, local_logs),
            daemon=True
        )
        t.start()

        tab1, tab2, tab3 = st.tabs(["🤖 Agent Logs", "📦 Content", "📊 Review"])

        with tab1:
            log_area = st.empty()
        with tab2:
            content_area = st.empty()
            content_area.info("⏳ Generating content…")
        with tab3:
            review_area = st.empty()
            review_area.info("⏳ Waiting for review…")

        while t.is_alive():
            drain_queue_to_list(local_logs)
            if local_logs:
                log_area.markdown(render_log_html(local_logs), unsafe_allow_html=True)
            time.sleep(0.5)

        t.join()
        drain_queue_to_list(local_logs)
        log_area.markdown(render_log_html(local_logs), unsafe_allow_html=True)

        st.session_state.logs = local_logs
        st.session_state.running = False

        if "error" in result_holder:
            st.error(f"Pipeline error: {result_holder['error']}")
        else:
            raw = result_holder.get("content", "")
            st.session_state.result = raw
            st.session_state.review = result_holder.get("review", "")

            b, s, e = parse_content_sections(raw)
            st.session_state.blog_content = b
            st.session_state.social_content = s
            st.session_state.email_content = e

            content_area.success("✅ Content ready — switch to the Content tab!")
            review_area.markdown(
                f'<div class="card">{markdown_to_html(st.session_state.review)}</div>',
                unsafe_allow_html=True
            )
        st.rerun()

REGEN_MARKERS = {
    "blog":   r'##\s*BLOG\s*POST\s*(.*?)(?=##\s*SOCIAL|##\s*EMAIL|$)',
    "social": r'##\s*SOCIAL\s*THREAD\s*(.*?)(?=##\s*BLOG|##\s*EMAIL|$)',
    "email":  r'##\s*EMAIL\s*TEASER\s*(.*?)(?=##\s*BLOG|##\s*SOCIAL|$)',
}
 
def extract_single_piece(raw: str, content_type: str) -> str:
    """Pull just the relevant section out of a single-piece writer response."""
    pattern = REGEN_MARKERS[content_type]
    m = re.search(pattern, raw, re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1).strip()
    # Fallback: the whole response is the piece (writer was told to return only one section)
    return raw.strip()
 
def _regen_thread(content_type, source, result_holder):
    try:
        raw = regenerate_piece(content_type, source, log_callback=add_log)
        result_holder["raw"] = raw
    except Exception as e:
        result_holder["error"] = str(e)

# ---------- Regenerate handler ----------
def do_regen(content_type):
    """Call regenerate_piece() for one piece only, then hot-swap it in session state."""
    source = st.session_state.source_text_snapshot or ""
    if not source.strip():
        st.warning("No source text to regenerate from.")
        return
 
    st.session_state[f"{content_type}_regen"] = True
    st.session_state[f"{content_type}_accepted"] = False
 
    while not log_queue.empty():
        log_queue.get()
 
    result_holder = {}
    t = threading.Thread(
        target=_regen_thread,
        args=(content_type, source, result_holder),
        daemon=True,
    )
    t.start()
 
    labels = {"blog": "Blog Post", "social": "Social Thread", "email": "Email Teaser"}
    with st.spinner(f"✍️ Regenerating {labels[content_type]}…"):
        while t.is_alive():
            time.sleep(0.5)
    t.join()
 
    # Drain any new logs into session
    new_logs = list(st.session_state.logs)
    drain_queue_to_list(new_logs)
    st.session_state.logs = new_logs
 
    if "error" in result_holder:
        st.error(f"Regeneration error: {result_holder['error']}")
    else:
        piece = extract_single_piece(result_holder.get("raw", ""), content_type)
        st.session_state[f"{content_type}_content"] = piece
 
    st.session_state[f"{content_type}_regen"] = False
    st.rerun()

# ---------- Show Results ----------
if st.session_state.result:
    tab1, tab2, tab3 = st.tabs(["🤖 Agent Logs", "📦 Content", "📊 Review"])

    # ── Logs ──
    with tab1:
        st.markdown(render_log_html(st.session_state.logs), unsafe_allow_html=True)

    # ── Content ──
    with tab2:

        # ── ZIP Export ──
        all_accepted = (
            st.session_state.blog_accepted and
            st.session_state.social_accepted and
            st.session_state.email_accepted
        )
        any_content = any([
            st.session_state.blog_content,
            st.session_state.social_content,
            st.session_state.email_content,
        ])

        if any_content:
            exp_col1, exp_col2 = st.columns([3, 1])
            with exp_col2:
                zip_bytes = build_zip(
                    st.session_state.blog_content,
                    st.session_state.social_content,
                    st.session_state.email_content,
                )
                accepted_count = sum([
                    st.session_state.blog_accepted,
                    st.session_state.social_accepted,
                    st.session_state.email_accepted,
                ])
                btn_label = f"📦 Export ZIP ({accepted_count}/3 accepted)" if not all_accepted else "📦 Export All as ZIP"
                st.download_button(
                    label=btn_label,
                    data=zip_bytes,
                    file_name="contentflow_export.zip",
                    mime="application/zip",
                    use_container_width=True,
                    type="primary" if all_accepted else "secondary",
                    help="Exports all 3 content pieces. Accept all to highlight this button.",
                )
            with exp_col1:
                if all_accepted:
                    st.success("🎉 All 3 pieces accepted — ready to export!")
                else:
                    st.info(f"Accept content pieces below to track approval. ({accepted_count}/3 accepted)")

        st.markdown("---")

        # ============================================================
        # SOCIAL MEDIA THREAD
        # ============================================================
        accepted_html = '<span class="accepted-badge">✓ Accepted</span>' if st.session_state.social_accepted else ""
        st.markdown(f'<div class="section-header"><h3 style="margin:0">🐦 Social Media Thread</h3>{accepted_html}</div>',
                    unsafe_allow_html=True)

        # Preview toggle
        preview_col1, preview_col2, preview_col3 = st.columns([1, 1, 4])
        with preview_col1:
            if st.button("📱 Mobile", key="social_mobile_btn",
                         type="primary" if st.session_state.social_preview_mobile else "secondary"):
                st.session_state.social_preview_mobile = True
                st.rerun()
        with preview_col2:
            if st.button("🖥️ Desktop", key="social_desktop_btn",
                         type="primary" if not st.session_state.social_preview_mobile else "secondary"):
                st.session_state.social_preview_mobile = False
                st.rerun()

        if st.session_state.social_content:
            if st.session_state.social_preview_mobile:
                st.markdown(render_social_mobile_preview(st.session_state.social_content),
                            unsafe_allow_html=True)
            else:
                st.markdown(
                    f'<div class="content-card">{markdown_to_html(st.session_state.social_content)}</div>',
                    unsafe_allow_html=True
                )
        else:
            st.markdown(
                f'<div class="content-card">{markdown_to_html(st.session_state.result)[:600]}…</div>',
                unsafe_allow_html=True
            )

        # Accept / Regenerate
        s_col1, s_col2, s_col3 = st.columns([1, 1, 4])
        with s_col1:
            if not st.session_state.social_accepted:
                if st.button("✅ Accept", key="social_accept", use_container_width=True):
                    st.session_state.social_accepted = True
                    st.rerun()
            else:
                if st.button("↩ Undo", key="social_undo", use_container_width=True):
                    st.session_state.social_accepted = False
                    st.rerun()
        with s_col2:
            if st.button("🔄 Regenerate", key="social_regen_btn", use_container_width=True,
                         disabled=st.session_state.social_regen):
                do_regen("social")

        st.markdown("---")

        # ============================================================
        # EMAIL NEWSLETTER
        # ============================================================
        accepted_html = '<span class="accepted-badge">✓ Accepted</span>' if st.session_state.email_accepted else ""
        st.markdown(f'<div class="section-header"><h3 style="margin:0">📧 Email Newsletter</h3>{accepted_html}</div>',
                    unsafe_allow_html=True)

        if st.session_state.email_content:
            st.markdown(
                f'<div class="content-card">{markdown_to_html(st.session_state.email_content)}</div>',
                unsafe_allow_html=True
            )

        e_col1, e_col2, e_col3 = st.columns([1, 1, 4])
        with e_col1:
            if not st.session_state.email_accepted:
                if st.button("✅ Accept", key="email_accept", use_container_width=True):
                    st.session_state.email_accepted = True
                    st.rerun()
            else:
                if st.button("↩ Undo", key="email_undo", use_container_width=True):
                    st.session_state.email_accepted = False
                    st.rerun()
        with e_col2:
            if st.button("🔄 Regenerate", key="email_regen_btn", use_container_width=True,
                         disabled=st.session_state.email_regen):
                do_regen("email")

        st.markdown("---")

        # ============================================================
        # BLOG POST
        # ============================================================
        accepted_html = '<span class="accepted-badge">✓ Accepted</span>' if st.session_state.blog_accepted else ""
        st.markdown(f'<div class="section-header"><h3 style="margin:0">📝 Blog Post</h3>{accepted_html}</div>',
                    unsafe_allow_html=True)

        # Preview toggle
        b_col1, b_col2, b_col3 = st.columns([1, 1, 4])
        with b_col1:
            if st.button("📱 Mobile", key="blog_mobile_btn",
                         type="primary" if st.session_state.blog_preview_mobile else "secondary"):
                st.session_state.blog_preview_mobile = True
                st.rerun()
        with b_col2:
            if st.button("🖥️ Desktop", key="blog_desktop_btn",
                         type="primary" if not st.session_state.blog_preview_mobile else "secondary"):
                st.session_state.blog_preview_mobile = False
                st.rerun()

        if st.session_state.blog_content:
            if st.session_state.blog_preview_mobile:
                st.markdown(render_blog_mobile_preview(st.session_state.blog_content),
                            unsafe_allow_html=True)
            else:
                st.markdown(render_blog_desktop_preview(st.session_state.blog_content),
                            unsafe_allow_html=True)
        else:
            st.markdown(
                f'<div class="content-card">{markdown_to_html(st.session_state.result)}</div>',
                unsafe_allow_html=True
            )

        # Accept / Regenerate
        bl_col1, bl_col2, bl_col3 = st.columns([1, 1, 4])
        with bl_col1:
            if not st.session_state.blog_accepted:
                if st.button("✅ Accept", key="blog_accept", use_container_width=True):
                    st.session_state.blog_accepted = True
                    st.rerun()
            else:
                if st.button("↩ Undo", key="blog_undo", use_container_width=True):
                    st.session_state.blog_accepted = False
                    st.rerun()
        with bl_col2:
            if st.button("🔄 Regenerate", key="blog_regen_btn", use_container_width=True,
                         disabled=st.session_state.blog_regen):
                do_regen("blog")

    # ── Review ──
    with tab3:
        st.markdown(
            f'<div class="card">{markdown_to_html(st.session_state.review)}</div>',
            unsafe_allow_html=True
        )