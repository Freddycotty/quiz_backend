from django.db import models
from apps.usuario.models import Usuarios
# Create your models here.
class Quiz(models.Model):
  nombre = models.CharField(max_length=50, unique=True, blank=False, null=False)
  descripcion = models.CharField(max_length=200, blank=True, null = True)
  created_at = models.DateTimeField('Fecha de Creacion',auto_now=False, auto_now_add=True)
  created_by = models.ForeignKey(Usuarios, on_delete=models.CASCADE,related_name='quiz_usuario', null = False)
  
  class Meta:
    verbose_name = 'quiz'
    verbose_name_plural = 'quiz'
    ordering = ['-id']
    db_table = 'quiz'
  
