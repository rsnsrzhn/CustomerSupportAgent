import asyncio
from src.services.email_service import EmailService
from src.services.ai_engine import AIEngine
from src.database.database import SessionLocal
from src.database.models import SupportLog
from src.core.config import settings

async def email_polling_worker():
    email_service = EmailService()
    ai_bot = AIEngine()
    
    MANAGER_EMAIL = settings.EMAIL_MANAGER

    while True:
        db = SessionLocal()
        try:
            new_letters = email_service.fetch_unread_emails()
            
            for letter in new_letters:
                raw_answer = ai_bot.get_answer(letter['body'])
                
                if "ESCALATE" in raw_answer:
                    status = "ESCALATED"
                    final_text = "Здравствуйте! Ваш запрос требует участия специалиста. Наш менеджер свяжется с вами в ближайшее время."

                    alert_subject = f"ALERT: Требуется помощь менеджера ({letter['sender']})"
                    alert_body = f"""
                    СРОЧНО: Клиент задал сложный вопрос.
                    Отправитель: {letter['sender']}
                    Тема: {letter['subject']}
                    Сообщение: {letter['body']}
                    """
                    email_service.send_answer(MANAGER_EMAIL, alert_subject, alert_body)
                else:
                    status = "COMPLETED"
                    final_text = raw_answer

                new_log = SupportLog(
                    user_email=letter['sender'],
                    message_text=letter['body'],
                    ai_answer=final_text,
                    status=status
                )
                db.add(new_log)
                db.commit()

                email_service.send_answer(
                    recipient=letter['sender'],
                    subject=letter['subject'],
                    text=final_text
                )
                print(f"[Worker] {status} - Email processed for {letter['sender']}")
                
        except Exception as e:
            print(f"[Worker Error] - {e}")
            db.rollback()
        finally:
            db.close()
            
        await asyncio.sleep(30)