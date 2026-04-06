import ReactMarkdown from "react-markdown"

export default function EmailPreview({ content, view }) {
  const cleanedContent = content.replace(/^##\s*EMAIL TEASER.*\n?/i, "")
  return (
    <div
      className={`bg-white rounded-xl shadow border p-4 
      transition-all duration-500 ease-in-out transform
      ${
        view === "mobile"
          ? "h-[70vh] overflow-y-auto max-w-93.75 mx-auto scale-[0.95]"
          : "h-auto scale-100"
      }`}
    >
      <div className="border-b pb-2 mb-3 text-sm text-gray-500">
        From: "Your Name"
      </div>

      <ReactMarkdown>{cleanedContent}</ReactMarkdown>
    </div>
  )
}