export default function SocialPreview({ content }) {
  const tweets = (content || "").split("\n\n").filter(Boolean)

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "8px", maxWidth: "480px" }}>
      {tweets.map((t, i) => (
        <div
          key={i}
          style={{
            background: "var(--color-background-primary)",
            border: "0.5px solid var(--color-border-tertiary)",
            borderRadius: "var(--border-radius-lg)",
            padding: "12px 14px",
            display: "flex",
            gap: "10px",
            alignItems: "flex-start",
          }}
        >
          <span
            style={{
              fontSize: "11px",
              fontWeight: "500",
              color: "var(--color-text-tertiary)",
              fontFamily: "var(--font-mono)",
              minWidth: "18px",
              paddingTop: "2px",
            }}
          >
            {i + 1}
          </span>
          <p style={{ margin: 0, fontSize: "14px", lineHeight: "1.6", color: "var(--color-text-primary)" }}>
            {t}
          </p>
        </div>
      ))}
    </div>
  )
}