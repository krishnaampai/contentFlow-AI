import ReactMarkdown from "react-markdown"

export default function EmailPreview({ content, view }) {
  return (
    <div className={`bg-white rounded-xl shadow border p-4 ${
      view === "mobile" ? "max-w-93.75 mx-auto" : "max-w-xl mx-auto"
    }`}>
      <div className="border-b pb-2 mb-3 text-sm text-gray-500">
        From: ContentFlow AI
      </div>

      <ReactMarkdown>{content}</ReactMarkdown>
    </div>
  )
}