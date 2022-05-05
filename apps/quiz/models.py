from django.db import models
from django.forms import BooleanField
from apps.usuario.models import Usuarios
# Create your models here.
class Quiz(models.Model):
  nombre = models.CharField(max_length=50, unique=True, blank=False, null=False)
  descripcion = models.CharField(max_length=200, blank=True, null = True)
  created_at = models.DateTimeField('Fecha de Creacion',auto_now=False, auto_now_add=True)
  created_by = models.ForeignKey(Usuarios, on_delete=models.CASCADE,related_name='quiz_usuario', null = True, blank=True)
  borrador = models.BooleanField(default=True)
  class Meta:
    verbose_name = 'quiz'
    verbose_name_plural = 'quiz'
    ordering = ['-id']
    db_table = 'quiz'
    
    def __str__(self) -> str:
      return str(self.nombre) or ""
  
class Preguntas(models.Model):
  nombre = models.CharField(max_length=50, unique=True, blank=False, null=False)
  detalle = models.CharField(max_length=250, unique=False, blank=False, null=False)
  valoracion = models.DecimalField(max_digits=10, decimal_places=1,blank=False, null=False)
  tiempo = models.IntegerField(blank=False, null=False)
  quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE,related_name='pregunta_quiz', null = False)
  class Meta:
    verbose_name = 'pregunta'
    verbose_name_plural = 'preguntas'
    ordering = ['-id']
    db_table = 'preguntas'
    
    def __str__(self) -> str:
      return str(self.nombre) or ""
    
class Respuestas(models.Model):
  detalle = models.CharField(max_length=250, unique=False, blank=False, null=False)
  verdadero = models.BooleanField()
  pregunta = models.ForeignKey(Quiz, on_delete=models.CASCADE,related_name='respuesta_pregunta', null = True)
  
  class Meta:
    verbose_name = 'respuesta'
    verbose_name_plural = 'respuestas'
    ordering = ['-id']
    db_table = 'respuestas'
  
  def __str__(self) -> str:
    return str(self.detalle) or ""

