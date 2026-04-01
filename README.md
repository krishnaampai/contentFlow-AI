# ContentFlow AI

---

##  The Problem

Creating high-quality marketing content across multiple formats (blogs, social media, emails) is time-consuming and often inconsistent. Most tools generate content in isolation without ensuring coherence, accuracy, or iterative improvement.

---

##  The Solution

ContentFlow AI is a multi-agent content generation system that automates the entire content pipeline. It uses specialized AI agents — a **Researcher**, **Writer**, and **Editor** — to collaboratively generate, refine, and validate content. The system produces multiple formats in one run and supports feedback-driven improvements, ensuring high-quality and consistent outputs.

---

##  Tech Stack

**Programming Languages**

* Python
* JavaScript

**Frameworks & Libraries**

* FastAPI (backend API)
* React + Vite (frontend)
* Tailwind CSS (styling)
* CrewAI (multi-agent orchestration)

**Tools & APIs**

* Gemini API (LLM)
* JSZip (export functionality)

---

##  Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/krishnaampai/contentFlow-AI
cd contentFlow-AI
```

---

### 2️⃣ Backend Setup (FastAPI)

```bash
cd backend
pip install -r requirements.txt
```

---

### 3️⃣ Add Environment Variables

Create a `.env` file in the backend folder:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

👉 Replace with your actual Gemini API key.

---

### 4️⃣ Run Backend Server

```bash
uvicorn main:app --reload
```

Server will run on:

```
http://localhost:8000
```

---

### 5️⃣ Frontend Setup (React + Vite)

```bash
cd frontend
npm install
```

---

### 6️⃣ Run Frontend

```bash
npm run dev
```

Frontend runs on:

```
http://localhost:5173
```

---

##  How to Use

1. Enter project details or content input
2. Click **Generate Content**
3. View:

   * Agent Logs
   * Generated Content (Blog, Social, Email)
   * Review section (side-by-side comparison)
4. Accept, regenerate, or export content

---

##  Key Features

* Multi-agent pipeline (**Researcher → Writer → Editor**)
* Generates blog, social thread, and email simultaneously
* Accept / Undo and Regenerate per section
* Side-by-side review comparison
* Export content as ZIP

---

##  Future Improvements

* File & URL input support
* Live streaming agent logs
* Database integration for history
* Authentication and user dashboards
