from django.template import Context
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings


def enviar_email(nombre, email):

    context = {
        'nombre': nombre,
        'email': email,
    }

    email_asunto = 'Gracias por registrarte en el quiz'
    email_data = render_to_string('email_mensaje.txt', context)

    email = EmailMessage(
        email_asunto, email_data,
        settings.DEFAULT_FROM_EMAIL, [email, ],
    )
    return email.send(fail_silently=False)