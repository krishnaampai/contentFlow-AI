export default function SocialPreview({ content, view }) {
  
  const posts = content.split(/\*\*Post \d+:\*\*/i).filter(Boolean)

  return (
    <div className={`space-y-4 ${view === "mobile" ? "max-w-93.75 mx-auto" : ""}`}>
      {posts.map((post, i) => (
        <div key={i} className="bg-white p-4 rounded-xl shadow border">
          <div className="flex items-center gap-2 mb-2">
            <div className="w-8 h-8 bg-gray-300 rounded-full"></div>
            <div className="text-sm font-medium">ContentFlow AI</div>
          </div>

          <p className="text-sm text-gray-800 whitespace-pre-line">
            {post.trim()}
          </p>

          <div className="flex gap-4 text-xs text-gray-500 mt-3">
            <span>Like</span>
            <span>Comment</span>
            <span>Share</span>
          </div>
        </div>
      ))}
    </div>
  )
}