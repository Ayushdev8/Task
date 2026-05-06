from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from decouple import config

def send_confirmation_email(user):
    subject = "Welcome to Our Platform 🎉"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [user.email]
    context = {
        "user": user,
    }
    text_content = f"Hi {user.username}, your account has been created successfully."
    email = EmailMultiAlternatives(
        subject,
        text_content,
        from_email,
        to_email,
    )
    template_uuid = config("MAILTRAP_TEMPLATE_UUID", default=None)
    if template_uuid:
        email.template_id = template_uuid

        # Dynamic data for Mailtrap template
        email.merge_data = {
            user.email: {
                "username": user.username,
            }
        }

    
        email.send(fail_silently=False)