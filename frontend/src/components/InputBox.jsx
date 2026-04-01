import { Textarea } from "@/components/ui/textarea"
import { Button } from "@/components/ui/button"
export default function InputBox({ input, setInput, onGenerate, loading }) {
  return (
    <div
      style={{
        background: "#1a1f2e",
        border: "0.5px solid #2d3748",
        borderRadius: "14px",
        padding: "16px",
      }}
    >
      <div style={{ display: "flex", gap: "12px", alignItems: "flex-end" }}>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Describe your content topic or paste a brief..."
          style={{
            flex: 1,
            background: "#0f1117",
            border: "0.5px solid #2d3748",
            borderRadius: "10px",
            padding: "12px 14px",
            color: "#e2e8f0",
            fontSize: "14px",
            lineHeight: "1.6",
            resize: "none",
            height: "80px",
            outline: "none",
            fontFamily: "inherit",
          }}
        />
        <button
          onClick={onGenerate}
          disabled={loading || !input.trim()}
          style={{
            background: loading ? "#1e3a5f" : "#2563eb",
            border: "none",
            borderRadius: "10px",
            padding: "0 24px",
            height: "80px",
            color: loading ? "#93c5fd" : "#fff",
            fontSize: "14px",
            fontWeight: "500",
            cursor: loading ? "not-allowed" : "pointer",
            whiteSpace: "nowrap",
            transition: "background 0.2s",
            minWidth: "140px",
          }}
        >
          {loading ? "Running..." : "Launch pipeline"}
        </button>
      </div>
    </div>
  )
}