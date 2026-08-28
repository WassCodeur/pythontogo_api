from smtplib import SMTP_SSL
import ssl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.core.settings import settings, logger
from app.utils.generate_email_htmal_format import generate_affiliation_email_content, generate_email_content, generate_team_email_content,  generate_ticket_team_email_content
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


def _send_mail_with_secondary_adress(to, text_msg, html_msg, subject, server=settings.admin_smtp_server, port=settings.admin_smtp_port, user=settings.admin_smtp_user, password=settings.admin_smtp_password, cc_list=None, bcc_list=None):
    msg = MIMEMultipart('alternative')

    msg['To'] = to
    msg['Subject'] = subject
    msg['From'] = f"PyCon Togo  2026 Team <{settings.smtp_user}>"
    msg['Cc'] = ', '.join(cc_list) if cc_list else ''
    msg['Bcc'] = ', '.join(bcc_list) if bcc_list else ''

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


def send_email_to_voluteering_team(name, email, message, date, phone=None):
    try:
        app_name = settings.business_name
        notification_type = "Volunteering Team Notification"
        title = "Someone wants to join the volunteering team"
        team_name = "Volunteering"
        subject = f"{name} has sent a message to the {team_name} - {app_name}"
        to = settings.volunteering_team_email
        date = date.strftime(
            "%Y-%m-%d %H:%M:%S") if hasattr(date, 'strftime') else str(date)
        email_html_content, email_plain_text_content = generate_team_email_content(
            app_name, team_name, notification_type, title, name, email, subject, date, message, phone)
        _send_mail_with_secondary_adress(to=to, text_msg=email_plain_text_content,
                                         html_msg=email_html_content, subject=subject)
    except Exception as e:
        logger.error(f"Failed to send team notification email to {to}: {e}")
        return


def send_email_to_ticketing_team(name, email, ticket_type, amount, payment_status, date, payment_url, voucher_code="N/A", phone="N/A"):
    try:
        app_name = settings.business_name
        title = f"{name} has paid for a ticket" if payment_status.lower(
        ) == "completed" else "Someone has initiated a ticket purchase"
        subject = f"{title} - {app_name}"
        to = settings.ticketing_team_email
        date = date.strftime(
            "%Y-%m-%d %H:%M:%S") if hasattr(date, 'strftime') else str(date)
        email_html_content, email_plain_text_content = generate_ticket_team_email_content(
            app_name, name, email, ticket_type, amount, payment_status, date, payment_url, voucher_code, phone)

        _send_mail_with_secondary_adress(to=to, text_msg=email_plain_text_content,
                                         html_msg=email_html_content, subject=subject)
    except Exception as e:
        import traceback
        traceback.print_exc()
        logger.error(
            f"Failed to send ticketing team notification email to {to}: {e}")
        return


def send_email_to_sponsorship_team(name, email, date, message, phone=None):
    try:
        to = settings.sponsorship_team_email
        app_name = settings.business_name
        team_name = "Sponsorship"
        notification_type = "Sponsorship Team Notification"
        title = "Someone wants to contact the sponsorship team"
        subject = f"{name} has sent a message to the {team_name} - {app_name}"
        date = date.strftime(
            "%Y-%m-%d %H:%M:%S") if hasattr(date, 'strftime') else str(date)

        email_html_content, email_plain_text_content = generate_team_email_content(
            app_name, team_name, notification_type, title, name, email, subject, date, message, phone)
        _send_mail_with_secondary_adress(to=to, text_msg=email_plain_text_content,
                                         html_msg=email_html_content, subject=subject)
    except Exception as e:
        logger.error(
            f"Failed to send sponsorship team notification email to {to}: {e}")
        return


def send_email_to_team(name, email, date, message, phone=None):
    try:
        to = settings.contact_team_email
        app_name = settings.business_name
        team_name = "Contact"
        notification_type = "Contact Team Notification"
        title = "Someone wants to contact the team"
        subject = f"{name} has sent a message to the {team_name} - {app_name}"
        date = date.strftime(
            "%Y-%m-%d %H:%M:%S") if hasattr(date, 'strftime') else str(date)
        email_html_content, email_plain_text_content = generate_team_email_content(
            app_name, team_name, notification_type, title, name, email, subject, date, message, phone)
        _send_mail_with_secondary_adress(to=to, text_msg=email_plain_text_content,
                                         html_msg=email_html_content, subject=subject)
    except Exception as e:
        logger.error(f"Failed to send team notification email to {to}: {e}")
        return


if __name__ == "__main__":

    # Version Texte Brut (text/plain)
    text_version = """Hi Fadima and the Team at Kabakoo,

    It was a real pleasure meeting you yesterday! Thank you for the warm welcome and for walking us through the incredible work you are doing around digital training and community building. The alignment between Kabakoo's vision and Python Togo's mission was clear, and we're truly excited about the potential of working together.

    As discussed, here is everything you need to consider supporting PyCon Togo 2026 (August 28-30, Lomé):

    1. Conference Program
    PyCon Togo 2026 runs across three days:
    - Day 1: Workshops, PyKids/DjangoKids, and beginner sessions
    - Day 2: Main conference (Keynotes, talks, lightning talks)
    - Day 3: Speakers' dinner and closing celebration

    Program details: https://docs.google.com/spreadsheets/d/1909716RL0dbj5hYG2y8ScKV1xwSGU25OXLD_VgiBob8/edit?gid=0#gid=0
    Speaker lineup: https://pycon.pytogo.org/speakers

    2. Event Overview & Last Year Report
    Event brochure: https://drive.google.com/file/d/1MxhdOtkcI1SGqr6qMhJiu8qV89jhmILp/view
    Last year report: https://report.pytogo.org
    Short highlight video: https://youtu.be/aU0v7jgyezk

    3. Budget Breakdown & Priority Need
    Budget breakdown: https://docs.google.com/spreadsheets/d/1YoYHr4aUms84cgGgul_4CpTA01u4eBW2R8EprTrYANc/edit?usp=sharing 

    One of our most critical line items is our food & beverage budget, covering meals and refreshments for around 300+ attendees, speakers, and volunteers across the 3 days. Any support here whether financial or in-kind would make a huge, visible impact on the attendee experience. That said, we remain completely open to any other form of support that suits Kabakoo best.

    We would be delighted to have you join us!

    Thank you again for your time and openness. Looking forward to building something impactful together.

    Best regards,

    Python Togo Team
    https://www.pytogo.org
    contact@pytogo.org
    PyCon Togo: https://pycon.pytogo.org/"""

    # Version HTML (text/html)
    html_version = """<div style="font-family: Arial, Helvetica, sans-serif; font-size: 14px; color: #222222; line-height: 1.5;">
    <p>Hi Fadima and the Kabakoo Team,</p>

    <p>It was a real pleasure meeting you yesterday! Thank you for the warm welcome and for walking us through the incredible work you are doing around digital training and community building. The alignment between Kabakoo's vision and Python Togo's mission was clear, and we're truly excited about the potential of working together.</p>

    <p>As discussed, here is everything you need to consider supporting <strong>PyCon Togo 2026</strong> (August 28-30, Lom&eacute;):</p>

    <p style="margin-bottom: 5px;"><strong>1. Conference Program</strong><br>
    PyCon Togo 2026 runs across three days:</p>
    <ul style="margin-top: 5px; margin-bottom: 10px; padding-left: 20px;">
        <li><strong>Day 1:</strong> Workshops, PyKids/DjangoKids, and beginner sessions</li>
        <li><strong>Day 2:</strong> Main conference (Keynotes, talks, lightning talks)</li>
        <li><strong>Day 3:</strong> Speakers and Partners dinner and closing celebration</li>
    </ul>
    <p style="margin-top: 0;">
        Program details: <a href="https://docs.google.com/spreadsheets/d/1909716RL0dbj5hYG2y8ScKV1xwSGU25OXLD_VgiBob8/edit?gid=0#gid=0" style="color: #1155cc;" target="_blank">Program draft</a><br>
        Speaker lineup: <a href="https://pycon.pytogo.org/speakers" style="color: #1155cc;" target="_blank">https://pycon.pytogo.org/speakers</a>
    </p>

    <p><strong>2. Event Overview &amp; Last Year Report</strong><br>
    Event brochure: <a href="https://drive.google.com/file/d/1MxhdOtkcI1SGqr6qMhJiu8qV89jhmILp/view" style="color: #1155cc;" target="_blank">https://drive.google.com/file/d/1MxhdOtkcI1SGqr6qMhJiu8qV89jhmILp/view</a><br>
    Last year report: <a href="https://report.pytogo.org" style="color: #1155cc;" target="_blank">https://report.pytogo.org</a><br>
    Short highlight video: <a href="https://youtu.be/aU0v7jgyezk" style="color: #1155cc;" target="_blank">https://youtu.be/aU0v7jgyezk</a></p>

    <p><strong>3. Budget Breakdown &amp; Priority Need</strong><br>
    Budget breakdown: <a href="https://docs.google.com/spreadsheets/d/1YoYHr4aUms84cgGgul_4CpTA01u4eBW2R8EprTrYANc/edit?usp=sharing" style="color: #1155cc;" target="_blank">Budget breakdown</a></p>

    <p>One of our most critical line items is our <strong>food &amp; beverage budget</strong>, covering meals and refreshments for around 300+ attendees, speakers, and volunteers across the 3 days. Any support here whether financial or in-kind would make a huge, visible impact on the attendee experience. That said, we remain completely open to any other form of support that suits Kabakoo best.</p>

    <p>We would be delighted to have you join us!</p>

    <p>Thank you again. Looking forward to building something impactful together.</p>

    <p>Best regards,</p>

    <p style="margin-bottom: 5px;">
        <strong>Python Togo Team</strong><br>
        <a href="https://www.pytogo.org" style="color: #1155cc;">https://www.pytogo.org</a><br>
        <a href="mailto:contact@pytogo.org" style="color: #1155cc;">contact@pytogo.org</a><br>
        PyCon Togo: <a href="https://pycon.pytogo.org/" style="color: #1155cc;">https://pycon.pytogo.org/</a>
    </p>
    </div>"""

    to = "wasscodeur228@gmail.com"

    cc_list = ["b.wachiou@pytogo.org", "l.geoffrey@pytogo.org"]
    _send_mail_with_secondary_adress(to=to, text_msg=text_version,
                                     html_msg=html_version, subject="[PyCon Togo 2026] Suite à notre échange - Python Togo x Kabakoo", cc_list=cc_list)
