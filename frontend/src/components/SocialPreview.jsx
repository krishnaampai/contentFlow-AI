export default function SocialPreview({ content, view }) {
  
  const posts = content.split(/\*\*Post \d+:\*\*/i).filter(Boolean)

  return (
    <div
      className={`space-y-4 transition-all duration-500 ease-in-out transform ${
        view === "mobile"
          ? "max-w-93.75 mx-auto h-[70vh] overflow-y-auto border p-4 rounded-xl scale-[0.95]"
          : "scale-100"
      }`}
    >
      {posts.map((post, i) => {
        const cleanedPost = post
          .trim()
          .replace(/^##\s*SOCIAL THREAD.*\n?/i, "")

        return (
          <div key={i} className="bg-white p-4 rounded-xl shadow border">
            <div className="flex items-center gap-2 mb-2">
              <div className="w-8 h-8 bg-gray-300 rounded-full"></div>
              <div className="text-sm font-medium">ContentFlow AI</div>
            </div>

            <p className="text-sm text-gray-800 whitespace-pre-line">
              {cleanedPost}
            </p>

            <div className="flex gap-4 text-xs text-gray-500 mt-3">
              <span>Like</span>
              <span>Comment</span>
              <span>Share</span>
            </div>
          </div>
        )
      })}
    </div>
  )
}