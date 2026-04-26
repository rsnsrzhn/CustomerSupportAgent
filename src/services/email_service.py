import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from src.core.config import settings

class EmailService:
    def __init__(self):
        self.user = settings.EMAIL_USER
        self.password = settings.EMAIL_PASSWORD

    def fetch_unread_emails(self) -> list:
        emails_data = []
        try:
            mail = imaplib.IMAP4_SSL(settings.IMAP_SERVER)
            mail.login(self.user,self.password)
            mail.select("inbox")

            status,response = mail.search(None,'UNSEEN')
            if status != 'OK' or not response[0]:
                return []
            
            for e_id in response[0].split():
                _,msg_data = mail.fetch(e_id,'(RFC822)')
                
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        subject = msg.get("subject",'Без темы')
                        sender = msg.get("from")
                        body = self._extract_body(msg)

                        emails_data.append({
                            "id": e_id,
                            "sender": sender,
                            "subject": subject,
                            "body" :body
                        })

            mail.logout()
        except Exception as e:
            print(f"Error IMAP:{e}")
        
        return emails_data
    
    def _extract_body(self,msg):
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    return part.get_payload(decode=True).decode()
        return msg.get_payload(decode=True).decode(errors='ignore')
    
    def send_answer(self,recipient:str,subject:str,text:str):
        try:
            msg = MIMEText(text)
            msg["Subject"] = f"Re: {subject}"
            msg["From"] = self.user
            msg["To"] = recipient

            with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
                server.starttls()
                server.login(self.user, self.password)
                server.send_message(msg)
        except Exception as e:
            print(f"SMTP error: {e}")

