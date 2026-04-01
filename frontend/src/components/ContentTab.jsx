import { useState } from "react"
import JSZip from "jszip"
import { Button } from "@/components/ui/button"
import ReactMarkdown from "react-markdown"

export default function ContentTab({ output }) {

  const [accepted, setAccepted] = useState({
    blog: false,
    social: false,
    email: false,
  })

  // --- parse content ---
 const parseContent = (text) => {
    const sections = {
      blog: "",
      social: "",
      email: "",
    }

    const blogMatch = text.match(/BLOG(?:\s+POST)?[:\n]+([\s\S]*?)(?=SOCIAL|EMAIL|$)/i)
    const socialMatch = text.match(/SOCIAL(?:\s+(?:THREAD|MEDIA))?[:\n]+([\s\S]*?)(?=BLOG|EMAIL|$)/i)
    const emailMatch = text.match(/EMAIL(?:\s+NEWSLETTER)?[:\n]+([\s\S]*?)(?=BLOG|SOCIAL|$)/i)

    sections.blog = blogMatch?.[1]?.trim() || ""
    sections.social = socialMatch?.[1]?.trim() || ""
    sections.email = emailMatch?.[1]?.trim() || ""

    return sections
  }
const { blog, social, email } = parseContent(output || "")

  // --- scroll helper ---
  const scrollTo = (id) => {
    document.getElementById(id)?.scrollIntoView({ behavior: "smooth" })
  }

  // --- zip export ---
  const exportZip = async () => {
    const zip = new JSZip()
    zip.file("blog.txt", blog)
    zip.file("social.txt", social)
    zip.file("email.txt", email)

    const blob = await zip.generateAsync({ type: "blob" })
    const link = document.createElement("a")
    link.href = URL.createObjectURL(blob)
    link.download = "contentflow.zip"
    link.click()
  }

  return (
    <div className="max-w-5xl mx-auto mt-10 space-y-8">

      {/* 🔥 TOP MENU */}
      <div className="sticky top-4 z-20 flex justify-between items-center 
      bg-white/60 backdrop-blur-xl border border-white/40 rounded-xl px-4 py-2 shadow-sm">

        {/* LEFT NAV */}
        <div className="flex gap-2">

          <button
            onClick={() => scrollTo("blog")}
            className="px-3 py-1 rounded-lg text-sm text-[#5b3a3a] hover:bg-white/50 z-10"
          >
            Blog
          </button>

          <button
            onClick={() => scrollTo("social")}
            className="px-3 py-1 rounded-lg text-sm text-[#5b3a3a] hover:bg-white/50"
          >
            Social
          </button>

          <button
            onClick={() => scrollTo("email")}
            className="px-3 py-1 rounded-lg text-sm text-[#5b3a3a] hover:bg-white/50"
          >
            Email
          </button>

        </div>

        {/* EXPORT */}
        <button
          onClick={exportZip}
          className="px-4 py-1.5 text-sm rounded-lg text-white 
          bg-gradient-to-r from-[#7f1d1d] via-[#dc2626] to-[#ea580c]"
        >
          Export ZIP
        </button>

      </div>

      {/* BLOG */}
      <Section
        id="blog"
        title="Blog"
        content={blog}
        accepted={accepted.blog}
        onAccept={() => setAccepted({ ...accepted, blog: !accepted.blog })}
      />

      {/* SOCIAL */}
      <Section
        id="social"
        title=" Social"
        content={social}
        accepted={accepted.social}
        onAccept={() => setAccepted({ ...accepted, social: !accepted.social })}
      />

      {/* EMAIL */}
      <Section
        id="email"
        title=" Email"
        content={email}
        accepted={accepted.email}
        onAccept={() => setAccepted({ ...accepted, email: !accepted.email })}
      />

    </div>
  )
}

// 🔹 Reusable section
function Section({ id, title, content, accepted, onAccept }) {
  return (
    <div id={id} className="bg-white/70 backdrop-blur-xl border rounded-xl p-5 space-y-4">

      {/* HEADER */}
      <div className="flex justify-between items-center">
        <h3 className="font-semibold text-[#4b2e2e]">{title}</h3>

        {accepted && (
          <span className="text-green-600 text-sm font-medium">
            ✓ Accepted
          </span>
        )}
      </div>

      {/* CONTENT */}
      <div className="prose prose-sm max-w-none text-[#3b2f2f]">
  <ReactMarkdown>
    {content}
  </ReactMarkdown>
</div>

      {/* ACTIONS */}
      <div className="flex gap-3">

        <Button
          onClick={onAccept}
          variant="outline"
        >
          {accepted ? "Undo" : "Accept"}
        </Button>

        <Button
          className="bg-gradient-to-r from-[#7f1d1d] via-[#dc2626] to-[#ea580c] text-white"
        >
          Regenerate
        </Button>

      </div>
    </div>
  )
}