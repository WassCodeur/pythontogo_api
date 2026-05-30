from smtplib import SMTP_SSL
import ssl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.core.settings import settings, logger
from app.utils.generate_email_htmal_format import generate_email_content
from fastapi import HTTPException, status
from app.utils.generate_ticket import generate_ticket
from app.utils.render_pass_email import render_pass_email


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
        return


async def send_email_for_confirme_your_ticket_purchase(to, action_url, action_text, first_name="Cher", last_name="Participant"):
    subject = f"Confirm Your PyCon Togo 2026 Ticket Purchase"
    greeting = f"Hello {first_name}"
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
        return


def send_email_new(to, text_msg, html_msg, subject):
    msg = MIMEMultipart('alternative')

    msg['To'] = to
    msg['Subject'] = subject
    msg['From'] = f"PyCon Togo  2026 Team <{settings.smtp_user}>"

    text_part = MIMEText(text_msg, 'plain')
    html_part = MIMEText(html_msg, 'html')

    msg.attach(text_part)
    msg.attach(html_part)

    context = ssl.create_default_context()

    with SMTP_SSL(host=settings.smtp_server, port=settings.smtp_port, context=context) as server:
        server.login(user=settings.smtp_user, password=settings.smtp_password)
        server.send_message(msg=msg)


def send_email_for_pass(to, first_name, full_name, ticket_id, number_of_slots=1, pass_type=""):
    if pass_type.lower() not in ["professional", "premium", "student", "diner"]:
        logger.error(f"Invalid pass type: {pass_type}")
        return
    subject = f"Your PyCon Togo 2026 {pass_type.capitalize()} Pass - Download Now"
    try:
        template_url = ""
        email_content = ""
        # Default to white, can be customized based on pass type
        name_color = (0, 0, 0, 225)
        color_id = (160, 160, 160, 255)  # Default to light gray
        pass_type = pass_type.lower()
        if pass_type == "professional":
            template_url = settings.professional_pass_template_url
            name_color = (136, 144, 247, 255)  # bleu lavande
            color_id = (160, 160, 160, 255)  # gris clair
        elif pass_type == "premium":
            template_url = settings.premium_pass_template_url
            name_color = (251, 152, 136, 255)  # rose saumon
            color_id = (160, 160, 160, 255)  # gris clair
        elif pass_type == "student":
            template_url = settings.student_pass_template_url
            name_color = (180, 230,  80, 255)  # vert lime
            color_id = (160, 160, 160, 255)  # gris clair
        elif pass_type == "dinner":
            template_url = settings.dinner_pass_template_url
            name_color = (251, 152, 136, 255)  # rose saumon
            color_id = (160, 160, 160, 255)  # gris clair
        else:
            logger.error(f"Invalid pass type: {pass_type}")
            return

        ticket_url, qr_url = generate_ticket(
            name=full_name, ticket_id=ticket_id, template_url=template_url, qr_data=f"Name: {full_name}\nTicket ID: {ticket_id}\nType: {pass_type.capitalize()}\nEvent: PyCon Togo 2026\nNumber of slots: {number_of_slots}", pass_type=pass_type, name_color=name_color, color_id=color_id)
        email_content = render_pass_email(
            pass_type, first_name, full_name, ticket_id, ticket_url, qr_url)
        send_email_new(to=to, text_msg="",
                       html_msg=email_content, subject=subject)
    except Exception as e:
        logger.error(f"Failed to send {pass_type} pass email to {to}: {e}")
        return


if __name__ == "__main__":
    send_email_for_pass(to="wasscodeur228@gmail.com", first_name="Wass",
                        full_name="Wasscodeur", ticket_id="1234567890", pass_type="professional")
