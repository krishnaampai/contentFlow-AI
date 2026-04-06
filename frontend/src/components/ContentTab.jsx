import { useState , useEffect} from "react"
import JSZip from "jszip"
import { Button } from "@/components/ui/button"
import ReactMarkdown from "react-markdown"
import ViewToggle from "./ViewToggle"
import BlogPreview from "./BlogPreview"
import SocialPreview from "./SocialPreview"
import EmailPreview from "./EmailPreview"
import { regenerateContent } from "../lib/api"
import AnimatedTabs from "./AnimatedTabs"
import { useRef } from "react"

export default function ContentTab({ output: initialOutput, input }) {

  const [logs, setLogs] = useState([])
  const [output, setOutput] = useState(initialOutput || "")
  const [activeTab, setActiveTab] = useState("blog")
  const [regenerating, setRegenerating] = useState({
    blog: false,
    social: false,
    email: false,
  })
  const regenRef = useRef("")

  useEffect(() => {
  setOutput(initialOutput || "")
},[initialOutput])
  const handleRegenerate = (type) => {
    setRegenerating(prev => ({ ...prev, [type]: true }))
    setLogs([])

    regenerateContent(input, type, {
      onLog: (log) => {
        console.log("LOG:", log)
        setLogs(prev => [...prev, log])
      },

      onOutput: (out) => {
  regenRef.current += "\n" + out

  setOutput(prev => {
    const live = regenRef.current

    if (type === "blog") {
      return prev.replace(
        /##\s*BLOG[\s\S]*?(?=##\s*SOCIAL|##\s*EMAIL|$)/i,
        `## BLOG POST\n${live}`
      )
    }

    if (type === "social") {
      return prev.replace(
        /##\s*SOCIAL[\s\S]*?(?=##\s*BLOG|##\s*EMAIL|$)/i,
        `## SOCIAL THREAD\n${live}`
      )
    }

    if (type === "email") {
      return prev.replace(
        /##\s*EMAIL[\s\S]*?(?=##\s*BLOG|##\s*SOCIAL|$)/i,
        `## EMAIL TEASER\n${live}`
      )
    }

    return prev
  })
},

      onDone: () => {
        const finalBuffer = regenRef.current
        regenRef.current = ""
        setOutput(prev => {
          if (!prev) return finalBuffer

          if (type === "blog") {
            return prev.replace(
              /##\s*BLOG[\s\S]*?(?=##\s*SOCIAL|##\s*EMAIL|$)/i,
              `## BLOG POST\n${finalBuffer.trim()}\n`
            )
          }

          if (type === "social") {
            return prev.replace(
              /##\s*SOCIAL[\s\S]*?(?=##\s*BLOG|##\s*EMAIL|$)/i,
              `## SOCIAL THREAD\n${finalBuffer.trim()}\n`
            )
          }

          if (type === "email") {
            return prev.replace(
              /##\s*EMAIL[\s\S]*?(?=##\s*BLOG|##\s*SOCIAL|$)/i,
              `## EMAIL TEASER\n${finalBuffer.trim()}\n`
            )
          }

          return prev
        })

        setRegenerating(prev => ({ ...prev, [type]: false }))
      },

      onError: () => {
        setRegenerating(prev => ({ ...prev, [type]: false }))
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

    const blogMatch = text.match(/##\s*BLOG[\s\S]*?(?=##\s*SOCIAL|##\s*EMAIL|$)/i)
    const socialMatch = text.match(/##\s*SOCIAL[\s\S]*?(?=##\s*BLOG|##\s*EMAIL|$)/i)
    const emailMatch = text.match(/##\s*EMAIL[\s\S]*?(?=##\s*BLOG|##\s*SOCIAL|$)/i)

    sections.blog = blogMatch?.[0]?.trim() || ""
    sections.social = socialMatch?.[0]?.trim() || ""
    sections.email = emailMatch?.[0]?.trim() || ""

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
    <div className="max-w-5xl mx-auto mt-10 px-6">
      {/* MENU */}<div className="sticky top-0 z-50 ">
      <div className="max-w-5xl mx-auto flex justify-between items-center 
  bg-white/60 backdrop-blur-sm  px-4 py-2 rounded-t-xl">

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
        isRegenerating={regenerating.blog}
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
        isRegenerating={regenerating.social}
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
        isRegenerating={regenerating.email}
      />

      

      {compareData && (
        <div className="fixed inset-0 z-9999 flex items-center justify-center">

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

function Section({ id, title, content, accepted, onAccept, input, onCompare, onRegenerate, isRegenerating }) {
  const [view, setView] = useState("desktop")
  return (
    <div id={id} className="bg-white/60 backdrop-blur-xl p-5 space-y-4">

      {/* HEADER */}
      <div className="sticky top-14 z-40 flex justify-between items-center bg-white/60 backdrop-blur-sm px-2 py-2 rounded-lg">
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
            disabled={isRegenerating}
            className="bg-linear-to-r from-[#7f1d1d] via-[#dc2626] to-[#ea580c] text-white"
          >
            {isRegenerating ? "Regenerating..." : "Regenerate"}
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