from rest_framework.routers import DefaultRouter
from .views import QuizViewset, PreguntasViewset,RespuestasViewset

router = DefaultRouter()

router.register('quiz', QuizViewset, basename='quiz')
router.register('preguntas', PreguntasViewset, basename='preguntas')
router.register('respuestas', RespuestasViewset, basename='respuestas')

urlpatterns = router.urls

