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

# ---------- Log Function ----------
def add_log(msg):
    st.session_state.logs.append(msg)

# ---------- Agent Status ----------
def get_status(agent):
    logs = " ".join(st.session_state.logs)

    if agent == "Researcher":
        if "Research completed" in logs:
            return "✅ Done"
        elif "Research started" in logs:
            return "⚡ Thinking"

    if agent == "Writer":
        if "Writing completed" in logs:
            return "✅ Done"
        elif "Writing attempt" in logs:
            return "⚡ Thinking"

    if agent == "Editor":
        if "Editing completed" in logs:
            return "✅ Done"
        elif "Editing started" in logs:
            return "⚡ Thinking"

    return "⏸ Idle"

# ---------- UI Header ----------
st.title("⚡ ContentFlow AI")
st.caption("Multi-Agent Content Factory")
st.markdown("---")

# ---------- Custom Theme ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: #e2e8f0;
}

h1, h2, h3 {
    color: #38bdf8;
}

.card {
    background: rgba(30, 41, 59, 0.7);
    backdrop-filter: blur(12px);
    border-radius: 20px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.1);
}
</style>
""", unsafe_allow_html=True)

# ---------- Input ----------
source_text = st.text_area("Paste Source Content", height=200)

# ---------- Agent Status ----------
st.markdown("### 🧠 Agent Status")
agents = ["Researcher", "Writer", "Editor"]
cols = st.columns(3)

for i, agent in enumerate(agents):
    cols[i].markdown(f"**{agent}**")
    cols[i].write(get_status(agent))

# ---------- Run Button ----------
if st.button("🚀 Launch Pipeline"):
    if not source_text.strip():
        st.warning("Please enter source content.")
    else:
        st.session_state.logs = []

        with st.spinner("Running ContentFlow AI... (may take 60–90s)"):
            final_content, final_review = run_pipeline(
                source_text,
                log_callback=add_log
            )

        st.session_state.result = final_content
        st.session_state.review = final_review

# ---------- Output Tabs ----------
if st.session_state.result:

    tab1, tab2, tab3 = st.tabs([
        "🤖 Agent Room",
        "📦 Content",
        "📊 Review"
    ])

    # ---------- Agent Room ----------
    with tab1:
        st.subheader("Live Agent Logs")

        for log in st.session_state.logs:
            if "❌" in log:
                color = "#ef4444"
            elif "✅" in log:
                color = "#22c55e"
            elif "🔍" in log or "🧠" in log or "✍️" in log:
                color = "#f59e0b"
            else:
                color = "#e5e7eb"

            st.markdown(
                f"<p style='color:{color}; font-family:monospace'>{log}</p>",
                unsafe_allow_html=True
            )

    # ---------- Content ----------
    with tab2:
        st.subheader("Generated Content")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write(st.session_state.result)
        st.markdown('</div>', unsafe_allow_html=True)

    # ---------- Review ----------
    with tab3:
        st.subheader("Editor Review")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write(st.session_state.review)
        st.markdown('</div>', unsafe_allow_html=True)