from rest_framework.routers import DefaultRouter
from .views import QuizViewset, PreguntasViewset,RespuestasViewset, EleccionesViewset

router = DefaultRouter()

router.register('quiz', QuizViewset, basename='quiz')
router.register('preguntas', PreguntasViewset, basename='preguntas')
router.register('respuestas', RespuestasViewset, basename='respuestas')
router.register('elecciones', EleccionesViewset, basename='elecciones')

urlpatterns = router.urls

