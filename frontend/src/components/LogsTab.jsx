import { useMemo } from "react"
import ContentTab from "./ContentTab"
export default function LogsTab({ logs, output }) {

  const currentStep = useMemo(() => {
    if (!logs) return "Waiting..."

    const lines = Array.isArray(logs)
      ? logs.map(l => l.trim())
      : typeof logs === "string"
        ? logs.split("\n").map(l => l.trim())
        : []
    let step = "Starting..."

    for (let line of lines) {

      if (/Research started/i.test(line)) {
        step = "Researching..."
      }

      else if (/Research completed/i.test(line)) {
        step = "Research complete"
      }

      else if (/Writing started/i.test(line)) {
        step = "Writing content..."
      }

      else if (/Writing attempt/i.test(line)) {
        step = line
      }

      else if (/Writing completed/i.test(line)) {
        step = "Writing complete"
      }

      else if (/Editing started/i.test(line)) {
        step = "Reviewing content..."
      }

      else if (/Editing completed/i.test(line)) {
        step = "Review complete"
      }

      else if (/All content approved/i.test(line)) {
        step = "Approved"
      }

      else if (/Pipeline finished/i.test(line)) {
        step = "Done"
      }
    }

    return step
  }, [logs])

  const isFinished = currentStep === "Done"

  return (
    <div className="max-w-3xl mx-auto mt-10 space-y-6">

      {/* 🔥 CURRENT STEP (rewriting UI) */}
      <div className="bg-white/70 backdrop-blur-xl border rounded-xl p-6 space-y-4">

        <AgentRow
          name="Researcher"
          active={currentStep.toLowerCase().includes("research")}
          done={currentStep.toLowerCase().includes("complete") || currentStep === "Done"}
          label={
            currentStep.toLowerCase().includes("research")
              ? "Researching..."
              : currentStep.toLowerCase().includes("research complete")
                ? "Done"
                : "Idle"
          }
        />

        <AgentRow
          name="Writer"
          active={currentStep.toLowerCase().includes("writing")}
          done={currentStep.toLowerCase().includes("writing complete") || currentStep === "Done"}
          label={
            currentStep.toLowerCase().includes("writing")
              ? currentStep
              : currentStep.toLowerCase().includes("writing complete")
                ? "Done"
                : "Idle"
          }
        />

        <AgentRow
          name="Editor"
          active={currentStep.toLowerCase().includes("review")}
          done={currentStep.toLowerCase().includes("approved") || currentStep === "Done"}
          label={
            currentStep.toLowerCase().includes("review")
              ? "Reviewing..."
              : currentStep.toLowerCase().includes("approved")
                ? "Approved"
                : "Idle"
          }
        />

      </div>

      {/* 🔥 SHOW CONTENT AFTER DONE */}
      {currentStep.toLowerCase().includes("done") && output && (
        <ContentTab output={output} />
      )}

    </div>
  )
}

function AgentRow({ name, active, done, label }) {
  return (
    <div className="flex items-center justify-between bg-white/60 rounded-lg px-4 py-3 border">

      {/* LEFT */}
      <div className="flex items-center gap-3">
        <div
          className={`w-2.5 h-2.5 rounded-full ${done
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

      {/* RIGHT */}
      <span
        className={`text-sm ${done
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