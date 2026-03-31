import time
import queue
import threading

from crew.crew import run_pipeline, regenerate_piece
from utils.content import decode_markdown, extract_single_piece

# Module-level queue shared between all threads and the UI polling loop
log_queue: queue.Queue = queue.Queue()

_SKIP_PHRASES = [
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


def should_show_log(msg: str) -> bool:
    stripped = msg.strip()
    if not stripped:
        return False
    return not any(phrase in stripped for phrase in _SKIP_PHRASES)


def add_log(msg: str) -> None:
    """Callback passed to crew — cleans and enqueues a log line."""
    clean = decode_markdown(msg)
    if should_show_log(clean):
        log_queue.put(clean)


def drain_queue(target: list) -> None:
    """Move everything currently in log_queue into target list."""
    while not log_queue.empty():
        target.append(log_queue.get())


def flush_queue() -> None:
    """Discard all pending log messages (call before a fresh run)."""
    while not log_queue.empty():
        log_queue.get()



def _full_pipeline_thread(source_text: str, result: dict) -> None:
    try:
        content, review = run_pipeline(source_text, log_callback=add_log)
        result["content"] = content
        result["review"] = review
    except Exception as e:
        result["error"] = str(e)


def run_pipeline_threaded(source_text: str, result: dict) -> threading.Thread:
    """Spawn and return a daemon thread running the full pipeline."""
    t = threading.Thread(target=_full_pipeline_thread, args=(source_text, result), daemon=True)
    t.start()
    return t



def _regen_thread(content_type: str, source: str, result: dict) -> None:
    try:
        raw = regenerate_piece(content_type, source, log_callback=add_log)
        result["raw"] = raw
    except Exception as e:
        result["error"] = str(e)


def run_regen_threaded(content_type: str, source: str, result: dict) -> threading.Thread:
    """Spawn and return a daemon thread regenerating a single content piece."""
    t = threading.Thread(target=_regen_thread, args=(content_type, source, result), daemon=True)
    t.start()
    return t


def poll_logs_until_done(thread: threading.Thread, log_list: list, sleep: float = 0.5) -> None:
    """Block-poll thread until finished, draining log_queue into log_list."""
    while thread.is_alive():
        drain_queue(log_list)
        time.sleep(sleep)
    thread.join()
    drain_queue(log_list)  # final drain