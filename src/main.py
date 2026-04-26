import asyncio
from fastapi import FastAPI
from fastapi.responses import RedirectResponse 
from src.api.router import router
from src.database.database import init_db
from src.services.worker import email_polling_worker

app = FastAPI(
    title="Customer Support AI",
    description="AI-powered email support system with logging and API access",
    version="1.0.0"
)

@app.on_event("startup")
async def on_startup():
    init_db()
    asyncio.create_task(email_polling_worker())

@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")

app.include_router(router)