import { motion } from "framer-motion"

export default function ViewToggle({ view, setView }) {
  const isMobile = view === "mobile"

  const toggle = () => {
    setView(isMobile ? "desktop" : "mobile")
  }

  return (
    <button
      onClick={toggle}
      className="flex items-center w-10 h-5 rounded-full p-1 bg-white/60 backdrop-blur border"
      style={{
        justifyContent: isMobile ? "flex-start" : "flex-end",
      }}
    >
      <motion.div
        layout
        transition={{
          type: "spring",
          stiffness: 300,
          damping: 20,
        }}
        className="w-3 h-3 rounded-full bg-linear-to-r from-[#7f1d1d] via-[#dc2626] to-[#ea580c]"
      />
    </button>
  )
}