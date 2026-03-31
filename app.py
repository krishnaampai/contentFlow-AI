import time
import streamlit as st

from utils.content import parse_content_sections, extract_single_piece, markdown_to_html
from utils.export import build_zip
from utils.pipeline import (
    flush_queue, drain_queue,
    run_pipeline_threaded, run_regen_threaded, poll_logs_until_done,
)
from ui.renderers import (
    APP_CSS, render_log_html,
    render_social_mobile_preview,
    render_blog_desktop_preview, render_blog_mobile_preview,
)

#  Page config 
st.set_page_config(page_title="ContentFlow AI", layout="wide")
st.markdown(APP_CSS, unsafe_allow_html=True)

#  Session state defaults 
DEFAULTS = {
    "result": None, "review": None, "logs": [], "running": False,
    "source_text_snapshot": "",
    "blog_content": "", "social_content": "", "email_content": "",
    "blog_accepted": False, "social_accepted": False, "email_accepted": False,
    "blog_regen": False, "social_regen": False, "email_regen": False,
    "social_preview_mobile": True, "blog_preview_mobile": False,
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

#  Header 
st.markdown("""
<div style="text-align:center;padding:20px 0 10px;">
  <h1 style="font-size:2.4rem;margin-bottom:4px;">⚡ ContentFlow AI</h1>
  <p style="color:#64748b;font-family:'DM Sans',sans-serif;font-size:1rem;margin:0;">
    Multi-Agent Content Factory — Generate · Review · Export
  </p>
</div>
""", unsafe_allow_html=True)
st.markdown("---")

#  Input
source_text = st.text_area("📄 Paste Source Content", height=180,
                            placeholder="Paste your article, brief, or notes here…")

# Launch pipeline 
if st.button(" Launch Pipeline", use_container_width=True, type="primary"):
    if not source_text.strip():
        st.warning("Please enter source content.")
    else:
        for key in [k for k in DEFAULTS if k != "source_text_snapshot"]:
            st.session_state[key] = DEFAULTS[key]
        st.session_state.source_text_snapshot = source_text
        st.session_state.running = True
        flush_queue()

        result_holder = {}
        local_logs = []
        thread = run_pipeline_threaded(source_text, result_holder)

        tab1, tab2, tab3 = st.tabs(["🤖 Agent Logs", "📦 Content", "📊 Review"])
        with tab1:
            log_area = st.empty()
        with tab2:
            content_area = st.empty()
            content_area.info("⏳ Generating content…")
        with tab3:
            review_area = st.empty()
            review_area.info("⏳ Waiting for review…")

        poll_logs_until_done(thread, local_logs)
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
            content_area.success(" ✅ Content ready — switch to the Content tab!")
            review_area.markdown(
                f'<div class="card">{markdown_to_html(st.session_state.review)}</div>',
                unsafe_allow_html=True,
            )
        st.rerun()


_REGEN_LABELS = {"blog": "Blog Post", "social": "Social Thread", "email": "Email Teaser"}

def do_regen(content_type: str) -> None:
    source = st.session_state.source_text_snapshot
    if not source.strip():
        st.warning("No source text to regenerate from.")
        return

    st.session_state[f"{content_type}_regen"] = True
    st.session_state[f"{content_type}_accepted"] = False
    flush_queue()

    result_holder = {}
    thread = run_regen_threaded(content_type, source, result_holder)

    with st.spinner(f"✍️ Regenerating {_REGEN_LABELS[content_type]}…"):
        while thread.is_alive():
            time.sleep(0.5)
    thread.join()

    new_logs = list(st.session_state.logs)
    drain_queue(new_logs)
    st.session_state.logs = new_logs

    if "error" in result_holder:
        st.error(f"Regeneration error: {result_holder['error']}")
    else:
        piece = extract_single_piece(result_holder.get("raw", ""), content_type)
        st.session_state[f"{content_type}_content"] = piece

    st.session_state[f"{content_type}_regen"] = False
    st.rerun()



def _section_title(emoji: str, label: str, accepted: bool) -> None:
    badge = '<span class="accepted-badge">✓ Accepted</span>' if accepted else ""
    st.markdown(
        f'<div class="section-header"><h3 style="margin:0">{emoji} {label}</h3>{badge}</div>',
        unsafe_allow_html=True,
    )

def _preview_toggle(ctype: str, key_prefix: str) -> None:
    mobile_key = f"{ctype}_preview_mobile"
    c1, c2, _ = st.columns([1, 1, 4])
    with c1:
        if st.button("📱 Mobile", key=f"{key_prefix}_mobile",
                     type="primary" if st.session_state[mobile_key] else "secondary"):
            st.session_state[mobile_key] = True
            st.rerun()
    with c2:
        if st.button("🖥️ Desktop", key=f"{key_prefix}_desktop",
                     type="primary" if not st.session_state[mobile_key] else "secondary"):
            st.session_state[mobile_key] = False
            st.rerun()

def _action_row(ctype: str, key_prefix: str) -> None:
    c1, c2, _ = st.columns([1, 1, 4])
    with c1:
        if not st.session_state[f"{ctype}_accepted"]:
            if st.button(" ✅ Accept", key=f"{key_prefix}_accept", use_container_width=True):
                st.session_state[f"{ctype}_accepted"] = True
                st.rerun()
        else:
            if st.button("↩ Undo", key=f"{key_prefix}_undo", use_container_width=True):
                st.session_state[f"{ctype}_accepted"] = False
                st.rerun()
    with c2:
        if st.button("🔄 Regenerate", key=f"{key_prefix}_regen",
                     use_container_width=True,
                     disabled=st.session_state[f"{ctype}_regen"]):
            do_regen(ctype)


#Results 
if st.session_state.result:
    tab1, tab2, tab3 = st.tabs(["🤖 Agent Logs", "📦 Content", "📊 Review"])

    with tab1:
        st.markdown(render_log_html(st.session_state.logs), unsafe_allow_html=True)

    with tab2:
        accepted_count = sum([st.session_state.blog_accepted,
                               st.session_state.social_accepted,
                               st.session_state.email_accepted])
        all_accepted = accepted_count == 3
        any_content = any([st.session_state.blog_content,
                           st.session_state.social_content,
                           st.session_state.email_content])

        # ZIP export bar
        if any_content:
            col_msg, col_btn = st.columns([3, 1])
            with col_btn:
                st.download_button(
                    label="📦 Export All as ZIP" if all_accepted
                          else f"📦 Export ZIP ({accepted_count}/3 accepted)",
                    data=build_zip(st.session_state.blog_content,
                                   st.session_state.social_content,
                                   st.session_state.email_content),
                    file_name="contentflow_export.zip",
                    mime="application/zip",
                    use_container_width=True,
                    type="primary" if all_accepted else "secondary",
                )
            with col_msg:
                if all_accepted:
                    st.success("🎉 All 3 pieces accepted — ready to export!")
                else:
                    st.info(f"Accept content pieces below. ({accepted_count}/3 accepted)")
        st.markdown("---")

        #SOCIAL 
        _section_title("🐦", "Social Media Thread", st.session_state.social_accepted)
        _preview_toggle("social", "social")
        if st.session_state.social_content:
            if st.session_state.social_preview_mobile:
                st.markdown(render_social_mobile_preview(st.session_state.social_content),
                            unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="content-card">'
                            f'{markdown_to_html(st.session_state.social_content)}</div>',
                            unsafe_allow_html=True)
        _action_row("social", "social")
        st.markdown("---")

        _section_title("📧", "Email Newsletter", st.session_state.email_accepted)
        if st.session_state.email_content:
            st.markdown(f'<div class="content-card">'
                        f'{markdown_to_html(st.session_state.email_content)}</div>',
                        unsafe_allow_html=True)
        _action_row("email", "email")
        st.markdown("---")

        _section_title("📝", "Blog Post", st.session_state.blog_accepted)
        _preview_toggle("blog", "blog")
        if st.session_state.blog_content:
            if st.session_state.blog_preview_mobile:
                st.markdown(render_blog_mobile_preview(st.session_state.blog_content),
                            unsafe_allow_html=True)
            else:
                st.markdown(render_blog_desktop_preview(st.session_state.blog_content),
                            unsafe_allow_html=True)
        _action_row("blog", "blog")

    with tab3:
        st.markdown(f'<div class="card">{markdown_to_html(st.session_state.review)}</div>',
                    unsafe_allow_html=True)