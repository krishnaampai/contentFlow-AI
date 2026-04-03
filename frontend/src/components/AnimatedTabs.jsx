import { motion } from "framer-motion"
import { useState } from "react"
const tabs = [
  { id: "blog", label: "Blog" },
  { id: "social", label: "Social" },
  { id: "email", label: "Email" },
]

export default function AnimatedTabs({ activeTab, setActiveTab }) {
  return (
    <div className="flex space-x-2 bg-white/40 backdrop-blur-md p-1 rounded-full w-fit">

      {tabs.map((tab) => (
        <button
          key={tab.id}
          onClick={() => {
            setActiveTab(tab.id)
            document.getElementById(tab.id)?.scrollIntoView({ behavior: "smooth" })
          }}
          className="relative px-4 py-1.5 text-sm font-medium rounded-full text-[#5b3a3a]"
          style={{ WebkitTapHighlightColor: "transparent" }}
        >
          {activeTab === tab.id && (
            <motion.span
              layoutId="bubble"
              className="absolute inset-0 bg-linear-to-r from-[#7f1d1d] via-[#dc2626] to-[#ea580c] z-0"
              style={{ borderRadius: 9999 }}
              transition={{ type: "spring", bounce: 0.2, duration: 0.5 }}
            />
          )}

          <span
            className={`relative z-10 ${
              activeTab === tab.id ? "text-white" : "text-[#5b3a3a]/70"
            }`}
          >
            {tab.label}
          </span>
        </button>
      ))}
    </div>
  )
}