from django.core.mail import send_mail
from django.conf import settings

def send_otp_via_email(email, otp):
    subject = 'Verification code from dating app '
    message = f'Your OTP code is {otp}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)

def send_password_via_email(email, new_password):
    subject = 'Password change from dating app '
    message = f'Your new password is {new_password}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)