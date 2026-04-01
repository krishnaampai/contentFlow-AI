import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from fastapi import FastAPI
from utils.pipeline import run_pipeline
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/generate")
async def generate(data: dict):
    input_text = data.get("input")

    logs = []

    def log_callback(msg):
        logs.append(msg)

    output, review = run_pipeline(input_text, log_callback)

    return {
        "logs": logs,
        "output": output,
        "review": review
    }