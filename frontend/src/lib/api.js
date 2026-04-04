const API = import.meta.env.VITE_API_URL

export const streamContent = (input, handlers) => {
  const eventSource = new EventSource(
    `${API}/generate-stream?input=${encodeURIComponent(input)}`
  )
  eventSource.onopen = () => console.log("CONNECTED");

  eventSource.onmessage = (event) => {
    console.log("MSG:", event.data);
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
    console.log("ERR:", e);
    eventSource.close()
    handlers.onError?.()
  }

  return eventSource
}

export const regenerateContent = (input, contentType, handlers) => {
  const eventSource = new EventSource(
    `${API}/regenerate-stream?content_type=${contentType}&input=${encodeURIComponent(input)}`
  )

  eventSource.onmessage = (event) => {
    const data = event.data

    if (data.startsWith("LOG::")) {
      handlers.onLog(data.replace("LOG::", ""))
    }

    else if (data.startsWith("OUTPUT::")) {
      handlers.onOutput(data.replace("OUTPUT::", ""))
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
