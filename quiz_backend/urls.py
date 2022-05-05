from django.contrib import admin
from django.urls import path, include
from apps.usuario.views import Login, Logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.usuario.urls')),
    path('api/', include('apps.quiz.urls')),
    # AUTENTICACION
    path('login/', Login.as_view(), name = 'login'),
    path('logout/', Logout.as_view(), name = 'logout'),
]
