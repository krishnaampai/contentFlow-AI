import { Textarea } from "@/components/ui/textarea"
import { Button } from "@/components/ui/button"
import { streamContent } from "./lib/api"
import { useState } from "react"
import LogsTab from "./components/LogsTab"
import ContentTab from "./components/ContentTab"
import dummyLogTxt from "./lib/dummyLogs.txt?raw"

export default function App() {

  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)
  const [logs, setLogs] = useState([])
  const [output, setOutput] = useState("")
  const [review, setReview] = useState("")
  const [activeTab, setActiveTab] = useState("logs")
  const [currentStep, setCurrentStep] = useState("")


const handleGenerate = () => {
  if (!input.trim()) return

  setLoading(true)
  setActiveTab("logs")
  setLogs([])
  setOutput("")
  setReview("")

  streamContent(input, {
    onLog: (log) => {
      setLogs(prev => [...prev, log])
    },

    onOutput: (out) => {
      console.log(out)
      setOutput(prev => prev + out + "\n")
      
    },

    onReview: (rev) => {
      setReview(prev => prev + "\n" + rev)
    },

    onDone: () => {
      setLoading(false)
    },

    onError: () => {
      setLoading(false)
    }
  })
}

  return (
    <div className="min-h-screen relative text-[#3b2f2f] px-10 py-10">

      
      {/* Base gradient */}
      <div className="absolute inset-0 z-0 bg-linear-to-br from-[#fff7ed] via-[#fde2e4] to-[#fef3c7]" />

      {/* Soft red/orange glow blobs */}
      <div className="fixed inset-0 -z-10">
        <div className="absolute -top-25 -left-25 w-100 h-100 bg-[#7f1d1d] opacity-20 blur-[120px] rounded-full z-0" />
      <div className="absolute -bottom-25 -right-25 w-100 h-100 bg-[#dc2626] opacity-20 blur-[120px] rounded-full z-0" />
      <div className="absolute top-[40%] left-[50%] w-75 h-75 bg-[#ea580c] opacity-20 blur-[100px] rounded-full z-0" />
      </div>
      

      {/* CONTENT */}
      <div className="relative z-10 max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-16 items-center">

        {/* LEFT SIDE */}
        <div className="space-y-6">

          <h1 className="text-6xl font-bold leading-tight 
          bg-linear-to-r from-[#7f1d1d] via-[#dc2626] to-[#ea580c] 
          bg-clip-text text-transparent">
            ContentFlow AI
          </h1>

          <p className="text-[#5b3a3a] text-lg max-w-lg">
            A multi-agent content generation platform that automates the creation of high-quality marketing content using AI. 
          </p>

        </div>

        {/* RIGHT SIDE CARD */}
        <div className="bg-white/70 backdrop-blur-xl border border-white/40 rounded-2xl p-6 shadow-xl space-y-5">

          <div className="flex justify-between items-center">
            <h3 className="font-semibold text-[#4b2e2e]">
              Enter project details or URL
            </h3>
          </div>

          <Textarea
              placeholder="Paste it here"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              className="min-h-35 bg-white/80 border border-[#f1d5d5] text-[#3b2f2f]"
          />

          <hr className="border-[#f1d5d5]" />

          <Button
            onClick={handleGenerate}
            disabled={loading}
            className="w-full h-12 text-white text-base rounded-xl 
            bg-linear-to-r from-[#7f1d1d] via-[#dc2626] to-[#ea580c] 
            hover:opacity-90 shadow-md"
          >
            {loading ? "Generating..." : "Generate Content →"}
          </Button>

        </div>
      </div>
      {/* BELOW HERO SECTION */}
      <div className="mt-16 flex flex-col items-center relative z-10">

        <div className="w-full mt-8 space-y-10">

          {/* LOGS */}
          <LogsTab logs={logs} output={output} input={input} />
         
        </div>
        <div className="w-full mt-8 space-y-10">
         {output && (
            <ContentTab output={output} input={input} />
          )}</div>

      </div>
    </div>
  )
}