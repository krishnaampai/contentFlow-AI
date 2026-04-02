import sys
import os
import asyncio
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from fastapi import FastAPI
from utils.pipeline import run_pipeline
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.get("/generate-stream-real")
# async def generate_stream_real(input: str):
#     async def event_generator():
#
#         def log_callback(msg):
#             yield_queue.append(msg)
#
#         yield_queue = []
#
#         async def run():
#             output, review = run_pipeline(input, log_callback)
#             return output, review
#
#         import asyncio
#         loop = asyncio.get_event_loop()
#         task = loop.run_in_executor(None, run_pipeline, input, log_callback)
#
#         while not task.done() or yield_queue:
#             while yield_queue:
#                 log = yield_queue.pop(0)
#                 yield f"data: LOG::{log}\n\n"
#
#             await asyncio.sleep(0.1)
#
#         output, review = await task
#
#         yield f"data: OUTPUT::{output}\n\n"
#         yield f"data: REVIEW::{review}\n\n"
#         yield f"data: DONE\n\n"
#
#     return StreamingResponse(event_generator(), media_type="text/event-stream")


@app.get("/generate-stream")
async def generate_stream(input: str):

    async def event_generator():
        logs = [
            "🔍 Research started",
            "✅ Research completed",
            "✍️ Writing started",
            "🧠 Writing attempt 1",
            "✅ Writing completed",
            "📝 Editing started",
            "✅ Editing completed",
            "🎉 All content approved!",
            "🏁 Pipeline finished"
        ]

        output = """
    ## BLOG POST
    ### Elevate Your Efficiency: Introducing DataSync Pro 3.0

    DataSync Pro 3.0 helps mid-market B2B SaaS companies cut data engineering costs by 60% and ship 3x faster. 
With real-time sync, 200+ connectors, and 99.7% accuracy, it transforms how teams handle data.DataSync Pro 3.0 helps mid-market B2B SaaS companies cut data engineering costs by 60% and ship 3x faster. 
With real-time sync, 200+ connectors, and 99.7% accuracy, it transforms how teams handle data.DataSync Pro 3.0 helps mid-market B2B SaaS companies cut data engineering costs by 60% and ship 3x faster. 
With real-time sync, 200+ connectors, and 99.7% accuracy, it transforms how teams handle data.DataSync Pro 3.0 helps mid-market B2B SaaS companies cut data engineering costs by 60% and ship 3x faster. 
With real-time sync, 200+ connectors, and 99.7% accuracy, it transforms how teams handle data.

    ---

    ## SOCIAL THREAD

    **Post 1:** 🚀 Struggling with slow data pipelines? Meet DataSync Pro 3.0.  
    **Post 2:** Cut costs by 60% & ship 3x faster.  
    **Post 3:** 200+ connectors + real-time sync.  
    **Post 4:** 99.7% accuracy + SOC2 certified.  
    **Post 5:** Launching April 15. Don’t miss it.

    ---

    ## EMAIL

    Subject: Cut Costs & Ship Faster 🚀

    Hey,  
    What if you could reduce data engineering costs by 60% and move 3x faster? 
DataSync Pro 3.0 makes it possible with AI-powered sync and 200+ integrations.
    """

        review = """
    BLOG: APPROVED  
    SOCIAL THREAD: APPROVED  
    EMAIL: APPROVED  

    OVERALL SCORE: 10/10  
    HALLUCINATIONS: NONE
    """

        for log in logs:
            yield f"data: LOG::{log}\n\n"
            await asyncio.sleep(1)

        for line in output.split("\n"):
            yield f"data: OUTPUT::{line}\n\n"
        for line in review.split("\n"):
            yield f"data: REVIEW::{line}\n\n"
        yield f"data: REVIEW::{review}\n\n"
        yield f"data: DONE\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")