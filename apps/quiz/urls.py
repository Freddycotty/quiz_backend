from rest_framework.routers import DefaultRouter
from .views import QuizViewset

router = DefaultRouter()

router.register('quiz', QuizViewset, basename='quiz')

urlpatterns = router.urls

