import { useState } from "react"
import JSZip from "jszip"
import { Button } from "@/components/ui/button"
import ReactMarkdown from "react-markdown"
import ViewToggle from "./ViewToggle"
import BlogPreview from "./BlogPreview"
import SocialPreview from "./SocialPreview"
import EmailPreview from "./EmailPreview"
import { regenerateContent } from "../lib/api"
import AnimatedTabs from "./AnimatedTabs"

export default function ContentTab({ output: initialOutput, input }) {

  const [loading, setLoading] = useState(false)
  const [logs, setLogs] = useState([])
  const [output, setOutput] = useState(initialOutput || "")
  const [regenBuffer, setRegenBuffer] = useState("")
  const [activeTab, setActiveTab] = useState("blog")

  const handleRegenerate = (type) => {
    setLoading(true)
    setLogs("")
    setRegenBuffer("")

    regenerateContent(input, type, {
      onLog: (log) => {
        console.log("LOG:", log)
        setLogs(prev => prev + (prev ? "\n" : "") + log)
      },

      onOutput: (out) => {
        console.log("OUTPUT:", out)
        setRegenBuffer(prev => prev + "\n" + out)
      },

      onDone: () => {
        setOutput(prev => {
          if (!prev) return regenBuffer

          if (type === "blog") {
            return prev.replace(
              /BLOG(?:\s+POST)?[:\n]+([\s\S]*?)(?=SOCIAL|EMAIL|$)/i,
              `BLOG POST:\n${regenBuffer.trim()}\n`
            )
          }

          if (type === "social") {
            return prev.replace(
              /SOCIAL(?:\s+(?:THREAD|MEDIA))?[:\n]+([\s\S]*?)(?=BLOG|EMAIL|$)/i,
              `SOCIAL THREAD:\n${regenBuffer.trim()}\n`
            )
          }

          if (type === "email") {
            return prev.replace(
              /EMAIL(?:\s+TEASER)?[:\n]+([\s\S]*?)(?=BLOG|SOCIAL|$)/i,
              `EMAIL TEASER:\n${regenBuffer.trim()}\n`
            )
          }

          return prev
        })

        setRegenBuffer("")
        setLoading(false)
      },

      onError: () => {
        setLoading(false)
      }
    })
  }

  const [accepted, setAccepted] = useState({
    blog: false,
    social: false,
    email: false,
  })
  const [compareData, setCompareData] = useState(null)
  console.log(input)

  const parseContent = (text) => {
    const sections = {
      blog: "",
      social: "",
      email: "",
    }

    const blogMatch = text.match(/BLOG(?:\s+POST)?[:\n]+([\s\S]*?)(?=SOCIAL|EMAIL|$)/i)
    const socialMatch = text.match(/SOCIAL(?:\s+(?:THREAD|MEDIA))?[:\n]+([\s\S]*?)(?=BLOG|EMAIL|$)/i)
    const emailMatch = text.match(/EMAIL(?:\s+TEASER)?[:\n]+([\s\S]*?)(?=BLOG|SOCIAL|$)/i)

    sections.blog = blogMatch?.[1]?.trim() || ""
    sections.social = socialMatch?.[1]?.trim() || ""
    sections.email = emailMatch?.[1]?.trim() || ""

    return sections
  }
  const { blog, social, email } = parseContent(output || "")

  const scrollTo = (id) => {
    document.getElementById(id)?.scrollIntoView({ behavior: "smooth" })
  }

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
    <div className="max-w-5xl mx-auto mt-10 space-y-8 px-6">

      {/* MENU */}<div className="sticky top-2 z-50">
      <div className="max-w-5xl mx-auto flex justify-between items-center 
  bg-white/60 backdrop-blur-sm rounded-xl px-4 py-2">

        <AnimatedTabs activeTab={activeTab} setActiveTab={setActiveTab} />

        <button
          onClick={exportZip}
          className="px-4 py-1.5 text-sm rounded-lg text-white 
          bg-linear-to-r from-[#7f1d1d] via-[#dc2626] to-[#ea580c] cursor-pointer"
        >
          Export ZIP
        </button>
      </div>
      </div>
      
      <Section
        id="blog"
        title="Blog"
        content={blog}
        accepted={accepted.blog}
        onAccept={() => setAccepted({ ...accepted, blog: !accepted.blog })}
        input={input}
        onCompare={() => setCompareData({ input, content: blog })}
        onRegenerate={() => handleRegenerate("blog")}
      />

      <Section
        id="social"
        title=" Social"
        content={social}
        accepted={accepted.social}
        onAccept={() => setAccepted({ ...accepted, social: !accepted.social })}
        input={input}
        onCompare={() => setCompareData({ input, content: social })}
        onRegenerate={() => handleRegenerate("social")}
      />
      <Section
        id="email"
        title=" Email"
        content={email}
        accepted={accepted.email}
        onAccept={() => setAccepted({ ...accepted, email: !accepted.email })}
        input={input}
        onCompare={() => setCompareData({ input, content: email })}
        onRegenerate={() => handleRegenerate("email")}
      />

      

      {compareData && (
        <div className="fixed inset-0 z-[9999] flex items-center justify-center">

          <div
            className="absolute inset-0 bg-black/40 backdrop-blur-md"
            onClick={() => setCompareData(null)}
          />

          <div className="relative w-[95%] max-w-7xl h-[90vh] bg-white rounded-2xl shadow-2xl flex flex-col overflow-hidden">

            <div className="flex justify-between items-center px-6 py-4 border-b">
              <h2 className="text-lg font-semibold">Compare Content</h2>
              <button onClick={() => setCompareData(null)}>✕</button>
            </div>

            <div className="grid md:grid-cols-2 gap-6 flex-1 overflow-hidden p-6">

              <div className="overflow-y-auto border rounded-xl p-4 bg-gray-50">
                <h4 className="text-sm font-semibold mb-3 text-gray-500">Original</h4>
                <p className="text-sm whitespace-pre-line">
                  {compareData.input}
                </p>
              </div>

              <div className="overflow-y-auto border rounded-xl p-4">
                <h4 className="text-sm font-semibold mb-3 text-gray-500">Generated</h4>
                <ReactMarkdown>{compareData.content}</ReactMarkdown>
              </div>

            </div>

          </div>

        </div>
      )}

    </div>
  )
}

function Section({ id, title, content, accepted, onAccept, input, onCompare, onRegenerate }) {
  const [view, setView] = useState("desktop")
  const [showCompare, setShowCompare] = useState(false)
  return (
    <div id={id} className="bg-white/70 backdrop-blur-xl border rounded-xl p-5 space-y-4">

      {/* HEADER */}
      <div className="sticky top-16 z-40 flex justify-between items-center bg-white/60 backdrop-blur-sm px-2 py-2 rounded-lg">
        <h3 className="font-semibold text-[#4b2e2e]">{title}</h3>

        <div className="flex gap-2">

          <Button
            onClick={onAccept}
            variant="outline"
            className="flex items-center gap-2"
          >
            {accepted && (
              <span className="text-green-600 text-sm">✓</span>
            )}
            {accepted ? "Accepted" : "Accept"}
          </Button>

          <Button
            onClick={onRegenerate}
            className="bg-linear-to-r from-[#7f1d1d] via-[#dc2626] to-[#ea580c] text-white"
          >
            Regenerate
          </Button>

          <Button
            className="bg-linear-to-r from-[#7f1d1d] via-[#dc2626] to-[#ea580c] text-white"
            onClick={onCompare}
          >
            Compare
          </Button>

        </div>
      </div>

      <div className="flex gap-2">
        <div className="flex items-center gap-2 text-xs text-[#5b3a3a]">
          <span>Mobile</span>
          <ViewToggle view={view} setView={setView} />
          <span>Desktop</span>
        </div>
      </div>

      {/* CONTENT */}
      <div className="w-full">
  <div className="mx-auto max-w-4xl">
    {title.trim().toLowerCase() === "email" && (
      <EmailPreview content={content} view={view} />
    )}


    {title.trim().toLowerCase() === "blog" && (
      <BlogPreview content={content} view={view} />
    )}

    {title.trim().toLowerCase() === "social" && (
      <SocialPreview content={content} view={view} />
    )}

    
  </div>
</div>

    </div>
  )
}