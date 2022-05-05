from rest_framework import serializers
from .models import Quiz, Preguntas, Respuestas

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
          'created_by': instance.created_by.id,
          'created_by_nombre': instance.created_by.nombre + ' '+ instance.created_by.apellido,
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
    pregunta_quiz = QuizSerializer(many=True, read_only=True)
    class Meta:
        model = Respuestas
        fields = '__all__'
    

    
 