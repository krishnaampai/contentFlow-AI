export default function BlogPreview({ content }) {
  return (
    <div
      style={{
        background: "var(--color-background-primary)",
        border: "0.5px solid var(--color-border-tertiary)",
        borderRadius: "var(--border-radius-lg)",
        padding: "1.5rem 1.75rem",
        color: "var(--color-text-primary)",
        fontSize: "15px",
        lineHeight: "1.8",
      }}
      dangerouslySetInnerHTML={{ __html: content }}
    />
  )
}