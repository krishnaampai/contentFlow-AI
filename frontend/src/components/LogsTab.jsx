export default function LogsTab({ logs }) {

  const getStyle = (line) => {
    const lower = line.toLowerCase()

    if (lower.includes("error")) return "text-red-600"
    if (lower.includes("completed") || lower.includes("approved")) return "text-green-600"
    if (lower.includes("started")) return "text-orange-500"
    if (lower.includes("output")) return "text-purple-600"

    return "text-[#4b2e2e]"
  }

  return (
    <div className="max-w-5xl mx-auto mt-10 relative z-10">

      <div className="bg-white/70 backdrop-blur-xl border border-white/40 rounded-xl p-6 shadow-sm space-y-3">

        {logs.length === 0 ? (
          <p className="text-[#6b4f4f] text-sm">
            No activity yet...
          </p>
        ) : (
          logs.map((line, i) => (
            <div
              key={i}
              className={`text-sm leading-relaxed ${getStyle(line)}`}
            >
              {line}
            </div>
          ))
        )}

      </div>
    </div>
  )
}