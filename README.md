# ContentFlow AI

---

##  The Problem

Creating high-quality marketing content across multiple formats (blogs, social media, emails) is time-consuming and often inconsistent. Most tools generate content in isolation without ensuring coherence, accuracy, or iterative improvement.

---

##  The Solution

ContentFlow AI is a multi-agent content generation system that automates the entire content pipeline. It uses specialized AI agents — a **Researcher**, **Writer**, and **Editor** — to collaboratively generate, refine, and validate content. The system produces multiple formats in one run and supports feedback-driven improvements, ensuring high-quality and consistent outputs.

---

## Tech Stack

**Programming Languages**

* Python  
* JavaScript  

**Frameworks & Libraries**

* FastAPI (backend API)  
* CrewAI (multi-agent orchestration)  
* React + Vite (frontend)  
* Tailwind CSS (styling)  
* BeautifulSoup4 (web scraping)  

**APIs & Third-party Tools**

* Gemini API (LLM)  
* SSE-Starlette (real-time streaming)  
* JSZip (export functionality)  

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
python -m venv venv

# Activate it
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

---

### 3️⃣ Add Environment Variables

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

👉 Replace with your actual Gemini API key.

### Frontend (.env)

Create a .env file inside the frontend folder:

```env
VITE_API_URL = http://localhost:8000
```

---

### 4️⃣ Run Backend Server from root

```bash
uvicorn backend.main:app --reload
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

1. Upload txt file or it's URL or directly use type project details
2. Click **Generate Content**
3. View:

   * Agent Logs (Researching, writing, editing)
   * Generated Content (Blog, Social, Email)
   * Compare section (side-by-side comparison)
4. Accept, regenerate, or export content

---

##  Key Features

* Multi-agent pipeline (**Researcher → Writer → Editor**) 
* Researcher generates a shared factsheet used across all content formats for consistency
* Editor can send content back to the Writer based on feedback (controlled by max_retries)
* Generates blog, social thread, and email simultaneously
* Accept / Undo and Regenerate per section
* Side-by-side review comparison
* Export content as ZIP
* Live streaming agent logs
* File & URL input support

---

##  Future Improvements

* Add user authentication and content history
* Improve UI with real-time typing animations
* Add comment-based regeneration for more precise edits
* Add an option to customize and apply a company’s tone across content

