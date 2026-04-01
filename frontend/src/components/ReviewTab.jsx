import ReactMarkdown from "react-markdown"

export default function ReviewTab({ input, output, review }) {

  // --- reuse parsing ---
  const parseContent = (text) => {
    const blogMatch = text.match(/BLOG(?:\s+POST)?[:\n]+([\s\S]*?)(?=SOCIAL|EMAIL|$)/i)
    const socialMatch = text.match(/SOCIAL(?:\s+(?:THREAD|MEDIA))?[:\n]+([\s\S]*?)(?=BLOG|EMAIL|$)/i)
    const emailMatch = text.match(/EMAIL(?:\s+NEWSLETTER)?[:\n]+([\s\S]*?)(?=BLOG|SOCIAL|$)/i)

    return {
      blog: blogMatch?.[1]?.trim() || "",
      social: socialMatch?.[1]?.trim() || "",
      email: emailMatch?.[1]?.trim() || "",
    }
  }

  const { blog, social, email } = parseContent(output || "")
  console.log("OUTPUT:", output)

  return (
    <div className="max-w-6xl mx-auto mt-10 grid md:grid-cols-2 gap-6">

      {/* LEFT: ORIGINAL */}
      <div className="bg-white/70 backdrop-blur-xl border rounded-xl p-5 space-y-4">
        <h3 className="font-semibold text-[#4b2e2e]">Original Input</h3>

        <div className="text-sm text-[#3b2f2f] whitespace-pre-wrap">
          {input || "No input"}
        </div>
      </div>

      {/* RIGHT: OUTPUT */}
      <div className="space-y-4">

        {/* BLOG */}
        <div className="bg-white/70 border rounded-xl p-4">
          <h4 className="text-[#7f1d1d] font-medium mb-2">Blog</h4>
          <div className="prose prose-sm max-w-none text-[#3b2f2f]">
            <ReactMarkdown>{blog}</ReactMarkdown>
          </div>
        </div>

        {/* SOCIAL */}
        <div className="bg-white/70 border rounded-xl p-4">
          <h4 className="text-[#dc2626] font-medium mb-2">Social</h4>
          <div className="prose prose-sm max-w-none text-[#3b2f2f]">
            <ReactMarkdown>{social}</ReactMarkdown>
          </div>
        </div>

        {/* EMAIL */}
        <div className="bg-white/70 border rounded-xl p-4">
          <h4 className="text-[#ea580c] font-medium mb-2">Email</h4>
          <div className="prose prose-sm max-w-none text-[#3b2f2f]">
            <ReactMarkdown>{email}</ReactMarkdown>
          </div>
        </div>

      </div>

      {/* REVIEW TEXT BELOW */}
      <div className="md:col-span-2 bg-white/70 border rounded-xl p-5 mt-4">
        <h3 className="font-semibold text-[#4b2e2e] mb-2">AI Review</h3>

        <div className="prose prose-sm max-w-none text-[#3b2f2f]">
          <ReactMarkdown>{review}</ReactMarkdown>
        </div>
      </div>

    </div>
  )
}