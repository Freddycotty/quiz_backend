from venv import create
from rest_framework import viewsets, status
from .models import Quiz, Preguntas, Respuestas
from .serializers import QuizSerializer, PreguntasSerializer, RespuestasSerializer
from rest_framework.response import Response

class QuizViewset(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    def create(self, request):
      quiz_serializer = self.serializer_class(data=request.data)
      if quiz_serializer.is_valid():
          quiz_serializer.save(borrador = True, created_by=request.user)
          return Response({
              'message': 'Quiz registrado correctamente.'
          }, status=status.HTTP_201_CREATED)
      return Response({
          'message': 'Error al momento de registral el Quiz',
          'errors': quiz_serializer.errors
      }, status=status.HTTP_400_BAD_REQUEST)
      
class PreguntasViewset(viewsets.ModelViewSet):
    queryset = Preguntas.objects.all()
    serializer_class = PreguntasSerializer
    
class RespuestasViewset(viewsets.ModelViewSet):
    queryset = Respuestas.objects.all()
    serializer_class = RespuestasSerializer
    
    def create(self, request):
      # EL CAMPO PREGUNTA DEBE ENVIARSE OBLIGATORIAMENTE
      if 'pregunta' not in request.data or request.data['pregunta'] == '' or request.data['pregunta'] == None:
        return Response({'message': 'El campo prgunta es obligatorio'}, status =status.HTTP_400_BAD_REQUEST) 
      
      
      verificacion_respuesta = Respuestas.objects.filter(pregunta_id = request.data['pregunta'])
      # Crear multiples respuesta a una pregunta
      if 'respuestas' in request.data:
        for i in request.data['respuestas']:
          
          # MAXIMO 4 RESPUESTAS POR PREGUNTAS
          if verificacion_respuesta.count() == 4:
            return Response({'message': 'El maximo de respuestas por pregunta son 4'}, status =status.HTTP_400_BAD_REQUEST)
          
          # VERIFICANDO QUE SOLO EXISTA UN VERDADERO PARA CADA PREGUNTA
          elif verificacion_respuesta.filter(verdadero = True) and i['verdadero'] == True:
            return Response({'message': 'Solo puede existir una respuesta verdadera para cada pregunta'}, status =status.HTTP_400_BAD_REQUEST)
          
          respuesta_serializer = self.serializer_class(data = i) 
          if respuesta_serializer.is_valid():
            respuesta_serializer.save(pregunta_id = request.data['pregunta'])
          else:
            return Response(respuesta_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
          
        return Response({'message': 'Las respuestas se crearon correctamente!.'}, status =status.HTTP_201_CREATED)
      
      # CREAR UNA RESPUESTA POR PREGUNTA
      else:
          if verificacion_respuesta.count() == 4:
            return Response({'message': 'El maximo de respuestas por pregunta son 4'}, status =status.HTTP_400_BAD_REQUEST)
          
          respuesta_serializer = self.serializer_class(data = request.data)
          if respuesta_serializer.is_valid():
            respuesta_serializer.save()
            return Response({'message': 'Respuesta creada correctamente!.'}, status =status.HTTP_201_CREATED)

      return Response(respuesta_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      