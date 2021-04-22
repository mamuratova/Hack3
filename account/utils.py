from django.core.mail import send_mail


def send_activation_code(email, activation_code):
    activation_url = f'http://localhost:8000/account/activate/{activation_code}/'
    message = f'Thank you for signing up!\n Please activate your account!\n Click here to activate: {activation_url}'
    send_mail('Apteka', message, 'test@test.com', [email, ], fail_silently=False)
