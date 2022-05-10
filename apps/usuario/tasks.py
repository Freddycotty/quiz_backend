from celery.utils.log import get_task_logger
from celery import shared_task

from .email import enviar_email

logger = get_task_logger(__name__)


@shared_task()
def email_registro(nombre, email):
    logger.info("Correo electronico enviado")
    return enviar_email(nombre, email)