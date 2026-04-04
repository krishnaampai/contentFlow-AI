import { useState } from "react"

export default function FactSheet({ factSheet }) {
  const [open, setOpen] = useState(true)

  if (!factSheet) return null

  return (
    <div className="max-w-3xl bg-white/70 backdrop-blur-xl shadow-2xl rounded-xl p-4 justify-center mx-auto">
        
      {/* Header */}
      <div className="flex justify-between items-center cursor-pointer"
           onClick={() => setOpen(!open)}>
        <h3 className="font-semibold text-[#4b2e2e]">Fact Sheet</h3>
        <span>{open ? "−" : "+"}</span>
      </div>

      {/* Content */}
      {open && (
        <pre className="mt-3 whitespace-pre-wrap text-sm">
          {factSheet}
        </pre>
      )}
    </div>
  )
}