from app.utils.dinner_mail_template import render_dinner_pass_email
from app.utils.student_mail_template import render_student_pass_email
from app.utils.pro_email_template import render_professional_pass_email
from app.utils.premium_mail_template import render_premium_pass_email


def render_pass_email(pass_type, first_name, full_name, ticket_id, ticket_url, qr_url):
    pass_type = pass_type.lower()
    if pass_type == "professional":
        return render_professional_pass_email(first_name, full_name, ticket_id, ticket_url, qr_url)
    elif pass_type == "premium":
        return render_premium_pass_email(first_name, full_name, ticket_id, ticket_url, qr_url)
    elif pass_type == "student":
        return render_student_pass_email(first_name, full_name, ticket_id, ticket_url, qr_url)
    elif pass_type == "dinner":
        return render_dinner_pass_email(first_name, full_name, ticket_id, ticket_url, qr_url)
    else:
        return
