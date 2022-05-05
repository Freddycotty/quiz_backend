from rest_framework import serializers
from .models import Usuarios

# USUARIO PARA EL LOGIN
class UsuarioTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuarios
        fields = ('email', 'nombre', 'apellido', 'is_active')

class UsuariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuarios
        fields = ['id', 'nombre', 'apellido', 'email']
        
class CrearUsuaroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuarios
        fields = ['id', 'nombre', 'apellido', 'email', 'password']
    
    def create(self,validated_data):
        user = Usuarios(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=128, min_length=6, write_only=True)

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {'password':'Debe ingresar ambas contraseñas iguales'}
            )
        return data
