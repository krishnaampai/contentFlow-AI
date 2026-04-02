import ReactMarkdown from "react-markdown"

export default function BlogPreview({ content, view }) {
  if (view === "mobile") {
    return (
      <div className="w-93.75 h-162.5 bg-black rounded-[2.5rem] p-2 shadow-2xl mx-auto">
        <div className="w-full h-full bg-white rounded-4xl overflow-hidden flex flex-col">
          <div className="h-6 flex justify-center items-center text-xs text-gray-500">9:41</div>
          <div className="px-4 py-2 border-b text-sm font-medium">Blog</div>
          <div className="flex-1 overflow-y-auto p-4">
            <div className="prose prose-sm max-w-none text-[#3b2f2f]">
              <ReactMarkdown>{content}</ReactMarkdown>
            </div>
          </div>
          <div className="h-10 border-t flex justify-center items-center text-gray-400">⬤</div>
        </div>
      </div>
    )
  }

  return (
    <div className="w-full max-w-4xl mx-auto bg-gray-200 rounded-xl shadow-inner p-4">
      <div className="flex items-center gap-2 mb-3">
        <div className="w-3 h-3 bg-red-400 rounded-full"></div>
        <div className="w-3 h-3 bg-yellow-400 rounded-full"></div>
        <div className="w-3 h-3 bg-green-400 rounded-full"></div>
        <div className="ml-3 text-xs text-gray-500 bg-white px-3 py-1 rounded-md">
          contentflow.ai/blog
        </div>
      </div>
      <div className="bg-white rounded-lg shadow p-6">
        <div className="prose max-w-none text-[#3b2f2f]">
          <ReactMarkdown>{content}</ReactMarkdown>
        </div>
      </div>
    </div>
  )
}