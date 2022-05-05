from rest_framework import serializers
from .models import Quiz, Preguntas, Respuestas, Elecciones

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'
        
    def to_representation(self, instance):
      data = {
          "id": instance.id,
          "nombre": instance.nombre,
          "descripcion": instance.descripcion,
          "borrador": instance.borrador,
          'created_at': str(instance.created_at)[0:19],
          'created_by_id': instance.created_by.id,
          'created_by': instance.created_by.nombre + ' '+ instance.created_by.apellido,
      }
      return data
    

class PreguntasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preguntas
        fields = '__all__'
 
    def to_representation(self, instance):
      data = {
          "id": instance.id,
          "nombre": instance.nombre,
          "detalle": instance.detalle,
          "valoracion": instance.valoracion,
          'tiempo': instance.tiempo,
          'posicion': instance.posicion,
          'quiz_id': instance.quiz.id,
          'quiz_nombre': instance.quiz.nombre,
      }
      return data

class RespuestasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Respuestas
        fields = '__all__'

class EleccionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Elecciones
        fields = '__all__'
        
    def to_representation(self, instance):
      data = {
          "id": instance.id,
          "quiz_id": instance.quiz.id,
          "quiz": instance.quiz.nombre,
          "pregunta_id": instance.pregunta.id,
          "pregunta": instance.pregunta.detalle,
          "respuesta_id": instance.respuesta.id if instance.respuesta is not None else None,
          "respuesta": instance.respuesta.detalle if instance.respuesta is not None else None,
          'usuario_id': instance.usuario.id,
          'usuario': instance.usuario.nombre + ' '+ instance.usuario.apellido,
          'respondido': instance.respondido,
          'puntaje': instance.puntaje,
      }
      return data
        
        