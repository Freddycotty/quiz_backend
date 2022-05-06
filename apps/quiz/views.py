from venv import create
from rest_framework import viewsets, status
from rest_framework.decorators import action
from .models import Quiz, Preguntas, Respuestas, Elecciones
from .serializers import QuizSerializer, PreguntasSerializer, RespuestasSerializer, EleccionesSerializer
from rest_framework.response import Response

class QuizViewset(viewsets.ModelViewSet):
    queryset = Quiz.objects
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
            return Response({'message': 'Ya se registro la respuesta verdadera y solo puede existir una!'}, status =status.HTTP_400_BAD_REQUEST)
          
          respuesta_serializer = self.serializer_class(data = i) 
          if respuesta_serializer.is_valid():
            respuesta_serializer.save(pregunta_id = request.data['pregunta'])
          else:
            return Response(respuesta_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
          
        return Response({'message': 'Las respuestas se crearon correctamente!.'}, status =status.HTTP_201_CREATED)
      
      # CREAR UNA RESPUESTA POR PREGUNTA
      else:
          # MAXIMO 4 RESPUESTAS POR PREGUNTAS
          if verificacion_respuesta.count() == 4:
            return Response({'message': 'El maximo de respuestas por pregunta son 4'}, status =status.HTTP_400_BAD_REQUEST)
          
          # VERIFICANDO QUE SOLO EXISTA UN VERDADERO PARA CADA PREGUNTA
          elif verificacion_respuesta.filter(verdadero = True) and request.data['verdadero'] == True:
            return Response({'message': 'Solo puede existir una respuesta verdadera para cada pregunta'}, status =status.HTTP_400_BAD_REQUEST)
          
          respuesta_serializer = self.serializer_class(data = request.data)
          if respuesta_serializer.is_valid():
            respuesta_serializer.save()
            return Response({'message': 'Respuesta creada correctamente!.'}, status =status.HTTP_201_CREATED)

      return Response(respuesta_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EleccionesViewset(viewsets.ModelViewSet):
  queryset = Elecciones.objects
  serializer_class = EleccionesSerializer

  def create(self, request):
      # ACUMULADOR
      acumulador = 0
      for i in self.queryset.filter(quiz_id = request.data['quiz']).values('puntaje',).all():
        acumulador =+ i['puntaje']
      
      # VERIFICACION PARA SABER SI EL USUARIO YA RESPONDIO LA PREGUNTA
      if self.queryset.filter(pregunta_id = request.data['pregunta']).first():
        return Response({'message': 'Esta pregunta ya fue respondida'}, status=status.HTTP_400_BAD_REQUEST)

      # VERIFICACION SI RESPONDE LA ULTIMA PREGUNTA PARA FINALIZAR EL QUIZ
      preguntal_last = Preguntas.objects.filter(quiz_id = request.data['quiz']).last()
      

      # SI EL USUARIO ENVIO UNA RESPUESTA
      if request.data['respondido']:
        respuesta = Respuestas.objects.filter(id=request.data['respuesta'], pregunta_id =request.data['pregunta'] ).first()

        # SI LA RESPUESTA ES VERDADERA
        if respuesta.verdadero:
          valor_pregunta = Preguntas.objects.filter(id = respuesta.pregunta_id).values('valoracion',).first()
          acumulador = acumulador + valor_pregunta['valoracion']
          eleccion_serializer = self.serializer_class(data=request.data)
          
          if eleccion_serializer.is_valid():
            eleccion_serializer.save(puntaje = valor_pregunta['valoracion'], usuario = request.user)
            # ENVIO DE CORREO
            if preguntal_last.id == request.data['pregunta']:
              print('enviar correo')
            
            return Response({
              'message': 'Respuesta correcta', 'puntaje': valor_pregunta['valoracion'], 'puntaje_total': acumulador
            }, status=status.HTTP_201_CREATED)
          
          return Response(eleccion_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
        # SI LA RESPUESTA NO ES VERDADERA
        else:
          eleccion_serializer = self.serializer_class(data=request.data)
          if eleccion_serializer.is_valid():
            eleccion_serializer.save(puntaje = 0, usuario = request.user)
            # ENVIO DE CORREO
            if preguntal_last.id == request.data['pregunta']:
              print('enviar correo')
            
            return Response({
              'message': 'UPPPS! Respuesta incorrecta', 'puntaje': 0, 'puntaje_total': acumulador
            }, status=status.HTTP_400_BAD_REQUEST)
          
          return Response(eleccion_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

      # SI EL USUARIO NO PUDO RESPONDER PORQUE SE LE EXCEDIO EL TIEMPO
      eleccion_serializer = self.serializer_class(data=request.data)
      if eleccion_serializer.is_valid():
        eleccion_serializer.save(puntaje = 0, usuario = request.user)
        # ENVIO DE CORREO
        if preguntal_last.id == request.data['pregunta']:
              print('enviar correo')
        
        return Response({
          'message': 'Se paso el tiempo, no respondiste', 'puntaje': 0, 'puntaje_total': acumulador
        }, status=status.HTTP_400_BAD_REQUEST)
      return Response(eleccion_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  #ELIMINAR TODOS LOS REGISTROS DE UN QUIZ PARA VOLVERLO HACER
  @action(detail=False, methods=['post'])
  def delete_elecciones(self, request):
      elecciones = self.queryset.filter(usuario_id = request.data['usuario'], quiz_id = request.data['quiz']).all()
      if elecciones:
        for i in elecciones:
          i.delete()
        return Response({'message': 'Todos tus registros en el Quiz han sido eliminados'}, status=status.HTTP_200_OK)
      return Response({
          'message': 'Hay errores en la información enviada'}, status=status.HTTP_400_BAD_REQUEST)