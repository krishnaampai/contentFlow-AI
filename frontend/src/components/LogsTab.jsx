import { useMemo } from "react"

const STEPS = {
  RESEARCHING: "researching",
  RESEARCH_DONE: "research_done",
  WRITING: "writing",
  WRITING_DONE: "writing_done",
  REVIEWING: "reviewing",
  REVIEW_DONE: "review_done",
  APPROVED: "approved",
  DONE: "done",
}

export default function LogsTab({ logs }) {

  const currentStep = useMemo(() => {
    if (!logs) return STEPS.RESEARCHING

    const lines = Array.isArray(logs)
      ? logs.map(l => l.trim())
      : typeof logs === "string"
        ? logs.split("\n").map(l => l.trim())
        : []

    let step = null

    for (let line of lines) {
      if (/Research started/i.test(line)) step = STEPS.RESEARCHING
      else if (/Research completed/i.test(line)) step = STEPS.RESEARCH_DONE
      else if (/Writing started/i.test(line)) step = STEPS.WRITING
      else if (/Writing attempt/i.test(line)) step = STEPS.WRITING
      else if (/Writing completed/i.test(line)) step = STEPS.WRITING_DONE
      else if (/Editing started/i.test(line)) step = STEPS.REVIEWING
      else if (/Editing completed/i.test(line)) step = STEPS.REVIEW_DONE
      else if (/All content approved/i.test(line)) step = STEPS.APPROVED
      else if (/Pipeline finished/i.test(line)) step = STEPS.DONE
    }

    return step
  }, [logs])

  return (
    <div className="max-w-3xl mx-auto mt-10 space-y-6">

      <div className="bg-white/70 backdrop-blur-xl shadow-2xl rounded-xl p-6 space-y-4">

        <AgentRow
          name="Researcher"
          active={currentStep === STEPS.RESEARCHING}
          done={[
            STEPS.RESEARCH_DONE,
            STEPS.WRITING,
            STEPS.WRITING_DONE,
            STEPS.REVIEWING,
            STEPS.REVIEW_DONE,
            STEPS.APPROVED,
            STEPS.DONE
          ].includes(currentStep)}
          label={
            currentStep === STEPS.RESEARCHING
              ? "Researching..."
              : currentStep === STEPS.RESEARCH_DONE
                ? "Done"
                : "Idle"
          }
        />

        <AgentRow
          name="Writer"
          active={currentStep === STEPS.WRITING}
          done={[
            STEPS.WRITING_DONE,
            STEPS.REVIEWING,
            STEPS.REVIEW_DONE,
            STEPS.APPROVED,
            STEPS.DONE
          ].includes(currentStep)}
          label={
            currentStep === STEPS.WRITING
              ? "Writing..."
              : currentStep === STEPS.WRITING_DONE
                ? "Done"
                : "Idle"
          }
        />

        <AgentRow
          name="Editor"
          active={currentStep === STEPS.REVIEWING}
          done={[
            STEPS.REVIEW_DONE,
            STEPS.APPROVED,
            STEPS.DONE
          ].includes(currentStep)}
          label={
            currentStep === STEPS.REVIEWING
              ? "Reviewing..."
              : currentStep === STEPS.APPROVED
                ? "Approved"
                : currentStep === STEPS.REVIEW_DONE
                  ? "Done"
                  : currentStep === STEPS.DONE
                    ? "Done"
                    : "Idle"
          }
        />

      </div>

    </div>
  )
}

function AgentRow({ name, active, done, label }) {
  return (
    <div className="flex items-center justify-between bg-white/60 rounded-lg px-4 py-3 border">

      <div className="flex items-center gap-3">
        <div
          className={`w-2.5 h-2.5 rounded-full ${
            done
              ? "bg-green-500"
              : active
                ? "bg-orange-500 animate-pulse"
                : "bg-gray-300"
          }`}
        />
        <span className="text-sm font-medium text-[#3b2f2f]">
          {name}
        </span>
      </div>

      <span
        className={`text-sm ${
          done
            ? "text-green-600"
            : active
              ? "text-gray-800 animate-pulse"
              : "text-gray-400"
        }`}
      >
        {done ? "Done" : active ? label : "Idle"}
      </span>

    </div>
  )
}