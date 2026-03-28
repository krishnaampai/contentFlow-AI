import re
import time
import queue
import threading
import streamlit as st
from crew.crew import run_pipeline

# ---------- Page Config ----------
st.set_page_config(page_title="ContentFlow AI", layout="wide")

# ---------- Session State ----------
if "result" not in st.session_state:
    st.session_state.result = None
if "review" not in st.session_state:
    st.session_state.review = None
if "logs" not in st.session_state:
    st.session_state.logs = []
if "running" not in st.session_state:
    st.session_state.running = False

# ---------- Log queue (module level) ----------
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

# ---------- Custom Theme ----------
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #0f172a, #1e293b); color: #e2e8f0; }
h1, h2, h3 { color: #38bdf8; }
.card {
    background: rgba(30, 41, 59, 0.7);
    backdrop-filter: blur(12px);
    border-radius: 20px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.1);
}
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.title("⚡ ContentFlow AI")
st.caption("Multi-Agent Content Factory")
st.markdown("---")

# ---------- Input ----------
source_text = st.text_area("Paste Source Content", height=200)

# ---------- Run Button ----------
if st.button("🚀 Launch Pipeline"):
    if not source_text.strip():
        st.warning("Please enter source content.")
    else:
        st.session_state.result = None
        st.session_state.review = None
        st.session_state.logs = []
        st.session_state.running = True

        while not log_queue.empty():
            log_queue.get()

        local_logs = []
        result_holder = {}

        def run_in_thread():
            try:
                fc, fr = run_pipeline(source_text, log_callback=add_log)
                result_holder["content"] = fc
                result_holder["review"] = fr
            except Exception as e:
                result_holder["error"] = str(e)

        t = threading.Thread(target=run_in_thread, daemon=True)
        t.start()

        tab1, tab2, tab3 = st.tabs(["🤖 Agent Logs", "📦 Content", "📊 Review"])

        with tab1:
            log_area = st.empty()
        with tab2:
            content_area = st.empty()
            content_area.info("⏳ Generating content...")
        with tab3:
            review_area = st.empty()
            review_area.info("⏳ Waiting for review...")

        while t.is_alive():
            while not log_queue.empty():
                local_logs.append(log_queue.get())
            if local_logs:
                log_area.markdown(render_log_html(local_logs), unsafe_allow_html=True)
            time.sleep(0.5)

        t.join()

        while not log_queue.empty():
            local_logs.append(log_queue.get())

        log_area.markdown(render_log_html(local_logs), unsafe_allow_html=True)

        st.session_state.logs = local_logs
        st.session_state.result = result_holder.get("content", "")
        st.session_state.review = result_holder.get("review", "")
        st.session_state.running = False

        if "error" in result_holder:
            st.error(f"Pipeline error: {result_holder['error']}")
        else:
            content_area.markdown(
                f'<div class="card">{markdown_to_html(st.session_state.result)}</div>',
                unsafe_allow_html=True
            )
            review_area.markdown(
                f'<div class="card">{markdown_to_html(st.session_state.review)}</div>',
                unsafe_allow_html=True
            )

# ---------- Show previous results ----------
elif st.session_state.result:
    tab1, tab2, tab3 = st.tabs(["🤖 Agent Logs", "📦 Content", "📊 Review"])

    with tab1:
        st.markdown(render_log_html(st.session_state.logs), unsafe_allow_html=True)

    with tab2:
        st.markdown(
            f'<div class="card">{markdown_to_html(st.session_state.result)}</div>',
            unsafe_allow_html=True
        )

    with tab3:
        st.markdown(
            f'<div class="card">{markdown_to_html(st.session_state.review)}</div>',
            unsafe_allow_html=True
        )