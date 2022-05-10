# PYTHON
from datetime import datetime
# DRF
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .tasks import email_registro

# DJANGO
from django.contrib.sessions.models import Session

#PROYECTO 
from .models import Usuarios
from .serializers import  UsuarioTokenSerializer, UsuariosSerializer, CrearUsuaroSerializer, PasswordSerializer

class UsuarioViewset(viewsets.ModelViewSet):
  model = Usuarios
  queryset = Usuarios.objects.filter(is_active=True).values('id', 'nombre', 'apellido', 'email')
  serializer_class = UsuariosSerializer

  # PUT
  def update(self, request, pk=None):
          usuario = self.model.objects.filter(id=pk).first()
          usuario_serializer = UsuariosSerializer(usuario, data=request.data)
          if usuario_serializer.is_valid():
              usuario_serializer.save(updated_by = request.user)
              return Response({
                  'message': 'Usuario actualizado correctamente'
              }, status=status.HTTP_200_OK)
          return Response({
              'message': 'Hay errores en la actualización',
              'errors': usuario_serializer.errors
          }, status=status.HTTP_400_BAD_REQUEST)
  #POST
  def create(self, request):
      usuario_serializer = CrearUsuaroSerializer(data=request.data)
      if usuario_serializer.is_valid():
          usuario_serializer.save()
          email_registro.delay('freddy', 'freddycarrillo1912@gmail.com')
          return Response({
              'message': 'Usuario registrado correctamente.'
          }, status=status.HTTP_201_CREATED)
      return Response({
          'message': 'Hay errores en el registro',
          'errors': usuario_serializer.errors
      }, status=status.HTTP_400_BAD_REQUEST)
  # DELETE
  def destroy(self, request, pk=None):
        usuario = self.model.objects.filter(id=pk).update(is_active=False)
        if usuario == 1:
            return Response({
                'message': 'Usuario eliminado correctamente'
            })
        return Response({
            'message': 'No existe el usuario que desea eliminar'
        }, status=status.HTTP_404_NOT_FOUND)
  #CAMBIAR CONTRASEÑA
  @action(detail=True, methods=['post'])
  def update_password(self, request, pk=None):
      usuario = self.model.objects.filter(id=pk).first()
      password_serializer = PasswordSerializer(data=request.data)
      if password_serializer.is_valid():
          usuario.set_password(password_serializer.validated_data['password'])
          usuario.save()
          return Response({
              'message': 'Contraseña actualizada correctamente'
          })
      return Response({
          'message': 'Hay errores en la información enviada',
          'errors': password_serializer.errors
      }, status=status.HTTP_400_BAD_REQUEST)

class Login(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        # envia al serializer username and password
        login_serializer = self.serializer_class(
            data=request.data, context={'request': request})
        if login_serializer.is_valid():
            # login serializer retorna user en validated_data
            user = login_serializer.validated_data['user']
            if user.is_active == True:
                token, created = Token.objects.get_or_create(user=user)
                user_serializer = UsuarioTokenSerializer(user)
                if created:
                    return Response({
                        'token': token.key,
                        'user': user_serializer.data,
                        'message': 'Acceso exitoso.'
                    }, status=status.HTTP_200_OK)
                else:
                    all_sessions = Session.objects.filter(
                        expire_date__gte=datetime.now())
                    if all_sessions.exists():
                        for session in all_sessions:
                            session_data = session.get_decoded()
                            if user.id == session_data.get('_auth_user_id'):
                                session.delete()
                    token.delete()
                    token = Token.objects.create(user=user)
                    return Response({
                        'token': token.key,
                        'usuario': user_serializer.data,
                        'message': 'Acceso exitoso.'
                    }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Esta usuario no puede iniciar sesión'},
                                status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Nombre de usuario o contraseña incorrecta'},
                            status=status.HTTP_400_BAD_REQUEST)

class Logout(APIView):
  

    def get(self, request, *args, **kwargs):
        try:
            token = str(self.request.headers['Authorization'])[6:]
            token = Token.objects.filter(key=token).first()

            if token:
                user = token.user
                # delete all sessions for user
                all_sessions = Session.objects.filter()
                if all_sessions.exists():
                    for session in all_sessions:
                        session_data = session.get_decoded()
                        if user.id == session_data.get('_auth_user_id'):
                            session.delete()
                token.delete()
                session_message = 'session de usuario eliminada'
                token_message = 'token eliminado.'
                return Response({'token_message': token_message, 'session_message': session_message},
                                status=status.HTTP_200_OK)

            return Response({'error': 'no se pudo encontrar un usuario con estas credenciales.'},
                            status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error': 'no se encontró ningún token en la solicitud.'},
                            status=status.HTTP_409_CONFLICT)