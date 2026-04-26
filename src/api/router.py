from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from src.database.database import SessionLocal
from src.database.models import SupportLog
from src.api.schemas import QuestionRequest, AnswerResponse
from src.services.ai_engine import AIEngine

router = APIRouter(prefix="/api/v1", tags=["AI Support"])
ai_bot = AIEngine()

templates = Jinja2Templates(directory="src/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/logs", response_class=HTMLResponse)
async def view_logs(request: Request, db: Session = Depends(get_db)):
    logs = db.query(SupportLog).order_by(SupportLog.created_at.desc()).all()
    return templates.TemplateResponse("logs.html", {"request": request, "logs": logs})

@router.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    answer = ai_bot.get_answer(request.question)
    return AnswerResponse(answer=answer)