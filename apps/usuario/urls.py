from rest_framework.routers import DefaultRouter
from .views import UsuarioViewset

router = DefaultRouter()

router.register('usuarios', UsuarioViewset, basename='usuarios')

urlpatterns = router.urls

