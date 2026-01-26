from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile
from .serializers import UserSerializer  #ingImports]
from rest_framework.decorators import action



class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

@action(detail=False, methods=['get'])
def active(self, request):
    users = UserProfile.objects.filter(is_active=True)
    serializer = self.serializer_class(users, many=True)
    return Response(serializer.data)

