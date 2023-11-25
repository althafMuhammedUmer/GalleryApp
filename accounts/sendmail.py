from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from decouple import config


def sendEmailMessage(username, to_email, otp, company_name, mail_subject):
    
    try:
        context = {
            "username" : username,
            "to_email": to_email,
            "otp": otp,
            "company_name": company_name,
        }
        message = render_to_string('forgot_password_otp_template.html', context )

        send_mail = EmailMessage(mail_subject, message, to=[to_email])
        send_mail.content_subtype = "html"

        send_mail.send()

    except Exception as e:
        print(e)

    





