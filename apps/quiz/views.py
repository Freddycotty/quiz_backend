from rest_framework import viewsets, status
from .models import Quiz
from .serializers import QuizSerializer
from rest_framework.response import Response

class QuizViewset(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    def create(self, request):
      quiz_serializer = self.serializer_class(data=request.data)
      if quiz_serializer.is_valid():
          quiz_serializer.save(borrador = True)
          return Response({
              'message': 'Quiz registrado correctamente.'
          }, status=status.HTTP_201_CREATED)
      return Response({
          'message': 'Error al momento de registral el Quiz',
          'errors': quiz_serializer.errors
      }, status=status.HTTP_400_BAD_REQUEST)