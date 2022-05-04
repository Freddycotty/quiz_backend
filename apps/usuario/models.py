# DJANGO - v prueba 5.0
from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    def _create_user(self, email, nombre,apellido, password, is_staff, is_superuser, is_active, **extra_fields):
        usuario = self.model(
            email = email,
            nombre = nombre,
            apellido = apellido,
            is_staff = is_staff,
            is_superuser = is_superuser,
            is_active = True,
            **extra_fields
        )
        usuario.set_password(password)
        usuario.save(using=self.db)
        return usuario

    def create_user(self,email, nombre,apellido, password=None, **extra_fields):
        return self._create_user(email, nombre,apellido, password, False, False, True, **extra_fields)

    def create_superuser(self,email, nombre,apellido, password=None, **extra_fields):
        return self._create_user(email, nombre,apellido, password, True, True, True, **extra_fields)


class Usuarios(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=30, null=False)
    apellido = models.CharField(max_length=50, null=False)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default=False)  
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'apellido']


    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'
        ordering = ['-id']
        db_table = 'usuarios'

