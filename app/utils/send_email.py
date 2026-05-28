from smtplib import SMTP_SSL
import ssl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.core.settings import settings, logger
from app.utils.generate_email_htmal_format import generate_email_content
from fastapi import HTTPException, status


def send_email(to, first_message, second_message, subject, action_url, action_text, business_name=settings.business_name, greeting="Cher Utilisateur"):
    msg = MIMEMultipart('alternative')

    msg['To'] = to
    msg['Subject'] = subject
    msg['From'] = f"{business_name} <{settings.smtp_user}>"

    message = f"{first_message}\n\n{second_message}"

    html = generate_email_content(
        business_name=business_name, message_content=first_message, second_message_content=second_message, action_url=action_url, action_text=action_text, greeting=greeting)

    text_part = MIMEText(message, 'plain')
    html_part = MIMEText(html, 'html')

    msg.attach(text_part)
    msg.attach(html_part)

    context = ssl.create_default_context()

    with SMTP_SSL(host=settings.smtp_server, port=settings.smtp_port, context=context) as server:
        print(
            f"Attempting login for: {settings.smtp_user} on {settings.smtp_server}")
        server.login(user=settings.smtp_user, password=settings.smtp_password)
        server.send_message(msg=msg)


async def send_email_for_ticket_puchase_confirmation(to, action_url, action_text, first_name="Cher", last_name="Participant"):
    subject = f"Your PyCon Togo 2026 Ticket - Download Now"
    greeting = f"Hello {first_name},"
    first_message = """
                    Thank you for purchasing your ticket for PyCon Togo 2026.

                    We are excited to welcome you to an inspiring event bringing together developers, students, tech enthusiasts, and professionals from across the community.

                    Your ticket is attached to this email.

                    You can also download your ticket directly using the button below:
    """
    second_message = f"""If the button above does not work, please use the following link to access your ticket:

                {action_url}

                We look forward to seeing you at PyCon Togo 2026.

                """

    try:
        send_email(to=to, first_message=first_message, second_message=second_message,
                   subject=subject, action_url=action_url, action_text=action_text, greeting=greeting)
    except Exception as e:
        logger.error(f"Failed to send email to {to}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to send email")


async def send_email_for_confirme_your_ticket_purchase(to, action_url, action_text, first_name="Cher", last_name="Participant"):
    subject = f"Confirm Your PyCon Togo 2026 Ticket Purchase"
    greeting = f"Hello {first_name},"
    first_message = """
                    Thank you for purchasing your ticket for PyCon Togo 2026.

                    To complete your registration, please confirm your ticket purchase by clicking the button below:
                    """
    second_message = f"""If the button above does not work, please use the following link to confirm your ticket purchase:

                {action_url}

                We look forward to seeing you at PyCon Togo 2026.

                """

    try:
        send_email(to=to, first_message=first_message, second_message=second_message,
                   subject=subject, action_url=action_url, action_text=action_text, greeting=greeting)
    except Exception as e:
        logger.error(f"Failed to send email to {to}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to send email")
