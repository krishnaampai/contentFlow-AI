from crewai import Crew, Process
from agents.researcher import create_researcher
from agents.writer import create_writer
from agents.editor import create_editor
from tasks.research_tasks import research_task
from tasks.writing_tasks import writing_task, rewrite_task
from tasks.editing_tasks import editing_task

MAX_RETRIES = 3

def run_pipeline(source_text=None):
    print("\n" + "="*60)
    print("CONTENTFLOW AI — PIPELINE STARTING")
    print("="*60)

    # Create agents (reused across retries)
    researcher = create_researcher()
    writer = create_writer()
    editor = create_editor()

    #  Research 
    task1 = research_task(researcher)
    research_crew = Crew(
        agents=[researcher],
        tasks=[task1],
        process=Process.sequential,
        verbose=True
    )
    research_result = research_crew.kickoff()
    print("\n✅ RESEARCHER DONE\n")

    # Write + Edit loop
    current_writing_task = writing_task(writer, context_tasks=[task1])
    correction_note = None
    final_result = None

    for attempt in range(1, MAX_RETRIES + 1):
        print(f"\n{'='*60}")
        print(f" WRITING ATTEMPT {attempt}/{MAX_RETRIES}")
        print("="*60)

        # If retry, rewrite task with correction note
        if attempt > 1 and correction_note:
            current_writing_task = rewrite_task(
                writer,
                correction_note=correction_note,
                context_tasks=[task1]
            )

        # Run writer
        writing_crew = Crew(
            agents=[writer],
            tasks=[current_writing_task],
            process=Process.sequential,
            verbose=True
        )
        writing_result = writing_crew.kickoff()

        print(f"\n✅ WRITER DONE (attempt {attempt})\n")

        # Run editor
        edit_task = editing_task(editor, context_tasks=[task1, current_writing_task])
        editing_crew = Crew(
            agents=[editor],
            tasks=[edit_task],
            process=Process.sequential,
            verbose=True
        )
        edit_result = editing_crew.kickoff()

        edit_text = str(edit_result)
        print(f"\n✅ EDITOR DONE (attempt {attempt})\n")

        # Check if everything is approved
        all_approved = (
            "BLOG: APPROVED" in edit_text and
            "SOCIAL THREAD: APPROVED" in edit_text and
            "EMAIL: APPROVED" in edit_text
        )

        if all_approved:
            print(f"\n🎉 ALL CONTENT APPROVED on attempt {attempt}!")
            final_result = writing_result
            break
        else:
            # Extract correction note for next iteration
            correction_note = extract_correction_note(edit_text)
            print(f"\n🔄 EDITOR REJECTED — sending correction note to Writer...")
            print(f"Correction: {correction_note}\n")

            if attempt == MAX_RETRIES:
                print(f"\n⚠️  Max retries ({MAX_RETRIES}) reached. Using last draft.")
                final_result = writing_result

    return final_result, edit_result


def extract_correction_note(edit_text):
    """Pull out correction notes from the editor's response."""
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