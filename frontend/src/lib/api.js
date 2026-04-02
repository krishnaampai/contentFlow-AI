const API = "http://localhost:8000"

export const streamContent = (input, handlers) => {
  const eventSource = new EventSource(
    `${API}/generate-stream?input=${encodeURIComponent(input)}`
  )

  eventSource.onmessage = (event) => {
    const data = event.data

    if (data.startsWith("LOG::")) {
      handlers.onLog(data.replace("LOG::", ""))
    }

    else if (data.startsWith("OUTPUT::")) {
      handlers.onOutput(data.replace("OUTPUT::", ""))
    }

    else if (data.startsWith("REVIEW::")) {
      handlers.onReview(data.replace("REVIEW::", ""))
    }

    else if (data === "DONE") {
      handlers.onDone()
      eventSource.close()
    }
  }

  eventSource.onerror = () => {
    eventSource.close()
    handlers.onError?.()
  }

  return eventSource
}