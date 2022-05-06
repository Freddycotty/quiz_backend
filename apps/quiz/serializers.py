from rest_framework import serializers
from .models import Quiz, Preguntas, Respuestas, Elecciones

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'
        
    def to_representation(self, instance):
      acumulador = 0
      pregunta_cantidad = 0
      tiempo_limite = 0
      data = {
          "id": instance.id,
          "nombre": instance.nombre,
          "descripcion": instance.descripcion,
          "borrador": instance.borrador,
          'created_at': str(instance.created_at)[0:19],
          'created_by_id': instance.created_by.id,
          'created_by': instance.created_by.nombre + ' '+ instance.created_by.apellido,
          'puntuacion_quiz': {},
          'pregunta_cantidad': {},
          'tiempo_limite': {},
          'pregunta': [],
          
      }
      for i in instance.pregunta_quiz.all():
        data['pregunta'].append(
          {
            'id': i.id,
            'nombre': i.nombre,
            'detalle': i.detalle,
            'valoracion': i.valoracion,
            'tiempo': i.tiempo,
            'posicion': i.posicion,
            'respuesta': []
          }
        )
        acumulador = acumulador+ i.valoracion
        pregunta_cantidad = pregunta_cantidad + 1
        tiempo_limite = tiempo_limite + i.tiempo
        for pregunta_quiz in data['pregunta']:
          for j in i.respuesta_pregunta.filter(pregunta_id = pregunta_quiz['id']):
            pregunta_quiz['respuesta'].append(
              {
                'id': j.id,
                'detalle': j.detalle,
                'verdadero': j.verdadero
              }
            )
      data['puntuacion_quiz'] = acumulador
      data['pregunta_cantidad'] = pregunta_cantidad
      data['tiempo_limite'] = tiempo_limite
      return data
    



class RespuestasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Respuestas
        fields = '__all__'

class PreguntasSerializer(serializers.ModelSerializer):
    respuesta_pregunta = RespuestasSerializer(many=True, read_only=True)

    class Meta:
        model = Preguntas
        fields = ['id', 'nombre', 'detalle', 'valoracion', 'tiempo', 'posicion', 'quiz','photo', 'respuesta_pregunta']

    def validate_posicion(self, value):
        posicion = value
        quiz = self.context['request'].data['quiz']
        pregunta = Preguntas.objects.filter(posicion = posicion, quiz_id =quiz ).first()
        if pregunta:
           raise serializers.ValidationError(
                "Esta posicion ya esta escogida en una pregunta!.")
        return value

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
        