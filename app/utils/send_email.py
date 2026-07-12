from smtplib import SMTP_SSL
import ssl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.core.settings import settings, logger
from app.utils.generate_email_htmal_format import generate_affiliation_email_content, generate_email_content
from fastapi import HTTPException, status
from app.utils.generate_ticket import generate_ticket
from app.utils.render_pass_email import render_pass_email
from app.utils.student_proof_of_enrollment import render_student_proof_under_review_email


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

    if not text_msg and not html_msg:
        logger.error("Both text_msg and html_msg are empty. Email not sent.")
        return
    elif not text_msg:
        text_msg = "This email requires an HTML-compatible email client to view."
    elif not html_msg:
        html_msg = "<html><body><p>This email requires an HTML-compatible email client to view.</p></body></html>"
    text_part = MIMEText(text_msg, 'plain')
    html_part = MIMEText(html_msg, 'html')

    msg.attach(text_part)
    msg.attach(html_part)

    context = ssl.create_default_context()

    with SMTP_SSL(host=settings.smtp_server, port=settings.smtp_port, context=context) as server:
        server.login(user=settings.smtp_user, password=settings.smtp_password)
        server.send_message(msg=msg)


def _send_mail_with_secondary_adress(to, text_msg, html_msg, subject, server=settings.admin_smtp_server, port=settings.admin_smtp_port, user=settings.admin_smtp_user, password=settings.admin_smtp_password):
    msg = MIMEMultipart('alternative')

    msg['To'] = to
    msg['Subject'] = subject
    msg['From'] = f"PyCon Togo  2026 Team <{settings.smtp_user}>"

    if not text_msg and not html_msg:
        logger.error("Both text_msg and html_msg are empty. Email not sent.")
        return
    elif not text_msg:
        text_msg = "This email requires an HTML-compatible email client to view."
    elif not html_msg:
        html_msg = "<html><body><p>This email requires an HTML-compatible email client to view.</p></body></html>"
    text_part = MIMEText(text_msg, 'plain')
    html_part = MIMEText(html_msg, 'html')

    msg.attach(text_part)
    msg.attach(html_part)

    context = ssl.create_default_context()

    with SMTP_SSL(host=server, port=port, context=context) as server:
        server.login(user=user, password=password)
        server.send_message(msg=msg)


def send_email_for_pass(to, first_name, full_name, ticket_id, number_of_slots=1, pass_type=""):

    # TODO: Add validation for pass_type to ensure it is one of the expected values

    subject = f"Your PyCon Togo 2026 {pass_type.capitalize()} Pass - Download Now"
    try:
        template_url = ""
        email_content = ""
        # Default to white, can be customized based on pass type
        name_color = (0, 0, 0, 225)
        color_id = (160, 160, 160, 255)  # Default to light gray
        pass_type = pass_type.lower()
        if pass_type in ["professional", "profesional", "pro", "standard", "Professionnel"]:
            template_url = settings.professional_pass_template_url
            name_color = (136, 144, 247, 255)  # bleu lavande
            color_id = (160, 160, 160, 255)  # gris clair
        elif pass_type in ["premium", "premier", "premium_pass", "premier_pass", "full_access"]:
            template_url = settings.premium_pass_template_url
            name_color = (251, 152, 136, 255)  # rose saumon
            color_id = (160, 160, 160, 255)  # gris clair
        elif pass_type in ["student", "etudiant"]:
            template_url = settings.student_pass_template_url
            name_color = (180, 230,  80, 255)  # vert lime
            color_id = (160, 160, 160, 255)  # gris clair
        elif pass_type in ["diner", "dinner"]:
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
        import traceback
        traceback.print_exc()

        logger.error(f"Failed to send {pass_type} pass email to {to}: {e}")
        return


def send_email_for_student_proof_of_enrollment(to, first_name, full_name, proof_id, submission_date, document_name, document_url):
    subject = f"Your PyCon Togo 2026 Proof of Enrollment - Under Review"
    try:
        email_content = render_student_proof_under_review_email(
            first_name, full_name, proof_id, submission_date, document_name, document_url)
        send_email_new(to=to, text_msg="",
                       html_msg=email_content, subject=subject,)
    except Exception as e:
        logger.error(f"Failed to send proof of enrollment email to {to}: {e}")
        return


def send_email_for_affiliation(to, affiliate_name, ticket_name, commission_amount, purchase_date, referral_id, event_name):
    subject = f"New Affiliation Notification - {event_name}"
    try:
        email_html_content, email_plain_text_content = generate_affiliation_email_content(
            affiliate_name, ticket_name, commission_amount, purchase_date, referral_id, event_name)
        _send_mail_with_secondary_adress(to=to, text_msg=email_plain_text_content,
                                         html_msg=email_html_content, subject=subject)
    except Exception as e:
        logger.error(f"Failed to send affiliation email to {to}: {e}")
        return


if __name__ == "__main__":
    send_email_for_affiliation(to="vehon22103@acoxs.com", affiliate_name="John Doe", ticket_name="Professional Pass",
                               commission_amount="$10", purchase_date="2024-06-01", referral_id="REF123456", event_name="PyCon Togo 2026")
