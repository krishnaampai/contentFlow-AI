import sys
import io
import re

from crewai import Crew, Process
from agents.researcher import create_researcher
from agents.writer import create_writer
from agents.editor import create_editor
from tasks.research_tasks import research_task
from tasks.writing_tasks import writing_task, rewrite_task, regenerate_single_task
from tasks.editing_tasks import editing_task

MAX_RETRIES = 1


def strip_ansi(text):
    return re.sub(r'\x1b\[[0-9;]*m', '', text)

class StreamToCallback(io.TextIOBase):
    def __init__(self, callback):
        self.callback = callback
        self.buffer = ""

    def write(self, text):
        self.buffer += text
        while "\n" in self.buffer:
            line, self.buffer = self.buffer.split("\n", 1)
            if line.strip():
                self.callback(strip_ansi(line))
        return len(text)

    def flush(self):
        pass


def log(msg, log_callback):
    if log_callback:
        log_callback(msg)


def run_pipeline(source_text=None, log_callback=None):
    if log_callback:
        old_stdout = sys.stdout
        sys.stdout = StreamToCallback(log_callback)
    try:
        print("\n" + "="*60)
        print("CONTENTFLOW AI — PIPELINE STARTING")
        print("="*60)

        researcher = create_researcher()
        writer = create_writer()
        editor = create_editor()

        if source_text is None:
            from tasks.research_tasks import SOURCE_TEXT
            source_text = SOURCE_TEXT

        task1 = research_task(researcher, source_text)
        log("🔍 Research started", log_callback)
        research_crew = Crew(
            agents=[researcher],
            tasks=[task1],
            process=Process.sequential,
            verbose=True
        )
        research_result = research_crew.kickoff()
        log("✅ Research completed", log_callback)
        log(f"📋 Researcher output:\n{str(research_result.raw)}", log_callback)
        log("✍️ Writing started", log_callback)

        current_writing_task = writing_task(writer, context_tasks=[task1])
        correction_note = None
        final_result = None

        for attempt in range(1, MAX_RETRIES + 1):
            print(f"\n{'='*60}")
            log(f"✍️ Writing attempt {attempt}", log_callback)
            print("="*60)

            if attempt > 1 and correction_note:
                current_writing_task = rewrite_task(
                    writer,
                    correction_note=correction_note,
                    context_tasks=[task1]
                )

            writing_crew = Crew(
                agents=[writer],
                tasks=[current_writing_task],
                process=Process.sequential,
                verbose=True
            )
            writing_result = writing_crew.kickoff()
            log("✅ Writing completed", log_callback)
            log(f"📋 Writer output:\n{str(writing_result.raw)}", log_callback)

            log("🧠 Editing started", log_callback)
            edit_task = editing_task(editor, context_tasks=[task1, current_writing_task])
            editing_crew = Crew(
                agents=[editor],
                tasks=[edit_task],
                process=Process.sequential,
                verbose=True
            )
            edit_result = editing_crew.kickoff()

            edit_text = str(edit_result)
            log("✅ Editing completed", log_callback)
            log(f"📋 Editor output:\n{str(edit_result.raw)}", log_callback)

            all_approved = (
                "BLOG: APPROVED" in edit_text and
                "SOCIAL THREAD: APPROVED" in edit_text and
                "EMAIL: APPROVED" in edit_text
            )

            if all_approved:
                log("🎉 All content approved!", log_callback)
                final_result = writing_result
                break
            else:
                correction_note = extract_correction_note(edit_text)
                log("❌ Editor rejected content — retrying...", log_callback)
                print(f"Correction: {correction_note}\n")

                if attempt == MAX_RETRIES:
                    print(f"\n⚠️  Max retries ({MAX_RETRIES}) reached. Using last draft.")
                    final_result = writing_result

        log("🚀 Pipeline finished", log_callback)
        return str(final_result.raw), str(edit_result.raw)

    finally:
        if log_callback:
            sys.stdout = old_stdout

def regenerate_piece(content_type: str, source_text: str, log_callback=None):
    """
    Re-run ONLY the researcher + writer for a single content piece.
    content_type: 'blog' | 'social' | 'email'
    Returns the new raw text for that piece (just the labelled section).
    """
    if log_callback:
        old_stdout = sys.stdout
        sys.stdout = StreamToCallback(log_callback)
    try:
        log(f"🔍 Re-researching for {content_type} regeneration…", log_callback)
        researcher = create_researcher()
        writer = create_writer()
 
        task1 = research_task(researcher, source_text)
        research_crew = Crew(
            agents=[researcher],
            tasks=[task1],
            process=Process.sequential,
            verbose=True,
        )
        research_crew.kickoff()
        log("✅ Research done", log_callback)
 
        log(f"✍️ Writing new {content_type}…", log_callback)
        regen_task = regenerate_single_task(writer, content_type, context_tasks=[task1])
        writing_crew = Crew(
            agents=[writer],
            tasks=[regen_task],
            process=Process.sequential,
            verbose=True,
        )
        result = writing_crew.kickoff()
        log(f"✅ {content_type.capitalize()} regenerated", log_callback)
        return str(result.raw)
 
    finally:
        if log_callback:
            sys.stdout = old_stdout


def extract_correction_note(edit_text):
    lines = edit_text.split('\n')
    notes = []
    capture = False
    for line in lines:
        if 'Correction Note' in line or 'REJECTED' in line:
            capture = True
        if capture and line.strip():
            notes.append(line.strip())
        if capture and len(notes) > 6:
            break
    return ' | '.join(notes) if notes else edit_text[:300]