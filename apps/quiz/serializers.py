from rest_framework import serializers
from .models import Quiz

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'
        extra_kwargs = {
        'created_by': {
        'default': serializers.CurrentUserDefault()      
        }
    }
        
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
    
