
#  ContentFlow AI

ContentFlow AI is a multi-agent content generation platform that automates the creation of high-quality marketing content using AI. It orchestrates specialized agents to research, generate, and refine content in a structured pipeline.

---

##  Overview

ContentFlow AI is built around three coordinated agents:

* **Researcher** — gathers and structures relevant context
* **Writer** — generates content across multiple formats
* **Editor** — reviews outputs and provides feedback

This pipeline ensures content is not just generated, but iteratively improved for quality and consistency.

---

##  Features

* Multi-agent pipeline (**Researcher → Writer → Editor**)
* Generate multiple content formats in one run:

  *  Blog post
  *  Social media thread
  *  Email teaser
* Per-content controls:

  * ✅ Accept / Undo
  * 🔄 Regenerate individual pieces
* Feedback-driven retry loop
*  Real-time agent logs
*  Responsive preview (mobile + desktop)
*  Export all content as ZIP
---

## 🛠️ Tech Stack

* **Frontend:** Streamlit
* **AI Orchestration:** CrewAI
* **Core Logic:** Python (threading, regex parsing, HTML rendering)

---

## 📁 Project Structure

```bash

CONTENTFLOW-AI/
├── app.py                  # Main Streamlit UI
├── run.py                  # Entry script (optional runner)
├── .env                    # Environment variables
├── .gitignore
├── README.md
├── venv/                   # Virtual environment (ignored)
│
├── crew/
│   └── crew.py             # Agent definitions + pipeline logic
│
├── tasks/
│   ├── __init__.py
│   ├── research_tasks.py   # Research agent tasks
│   ├── writing_tasks.py    # Writer agent tasks
│   ├── editing_tasks.py    # Editor agent tasks
│
├── tools/                  # (Optional utilities for agents)
│
├── ui/
│   └── renderers.py        # UI rendering + previews
│
└── utils/
    ├── content.py          # Content parsing logic
    ├── export.py           # ZIP export functionality
    └── pipeline.py         # Threading + pipeline orchestration
```

---

## ⚙️ How It Works

1. User provides input (currently text)
2. **Researcher** processes and structures information
3. **Writer** generates:

   * Blog post
   * Social thread
   * Email teaser
4. **Editor** reviews and suggests improvements
5. System retries generation using feedback (if needed)
6. User can accept, regenerate, or export content

---

##  Future Improvements

* Support for file inputs (PDF, DOCX) and URLs
* Editor-driven regeneration loop for individual pieces
* Persistent storage (DB integration)
* Authentication and user dashboards

---

##  Getting Started

```bash
# Clone the repo
git clone <your-repo-url>

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

---
