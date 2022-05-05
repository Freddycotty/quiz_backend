from rest_framework.routers import DefaultRouter
from .views import QuizViewset, PreguntasViewset

router = DefaultRouter()

router.register('quiz', QuizViewset, basename='quiz')
router.register('preguntas', PreguntasViewset, basename='preguntas')

urlpatterns = router.urls

