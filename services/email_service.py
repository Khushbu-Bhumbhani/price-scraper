import smtplib
from email.mime.text import MIMEText
from config import EMAIL_PASSWORD,EMAIL_RECEIVER,EMAIL_SENDER
from typing import Optional
import logging

logger=logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def send_email(subject:str,body:str,receiver:Optional[str]=None)->None:
    """Send email notification

    Args:
        subject (str): Email Subject
        body (str): Email body
        receiver (Optional[str]): Override default receiver
    """
    recipient=receiver or EMAIL_RECEIVER
    msg=MIMEText(body)
    msg["Subject"]=subject
    msg["From"]=EMAIL_SENDER
    msg["To"]=recipient
    
    try:
        with smtplib.SMTP("smtp.gmail.com",587, timeout=10) as server:
            server.starttls()
            server.login(EMAIL_SENDER,EMAIL_PASSWORD)
            server.send_message(msg)
            
            logger.info(f"Email send successfully to {recipient}")
    except smtplib.SMTPAuthenticationError as e:
        logger.error("Authentication Failed. Check email/password (App password required)")
        raise
    except smtplib.SMTPException as e:
        logger.error(f"SMTP error occurred: {e}")
        raise
    except Exception as e:
        logger.exception(f"Unexpected error while sending email:  {e}")
        raise
        