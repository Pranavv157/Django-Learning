from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import UserProfile
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAdminUser
from django.contrib.auth.models import User
from rest_framework.views import APIView
from .permissions import IsOwner




class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        User.objects.create_user(username=username, password=password)

        return Response(
            {"message": "User created successfully"},
            status=status.HTTP_201_CREATED
        )

class UserViewSet(viewsets.ModelViewSet):

    # 1. Default queryset → only active users
    queryset = UserProfile.objects.filter(is_active=True)

    #  2. Serializer
    serializer_class = UserSerializer
    
    def get_permissions(self):

        if self.action == "destroy":
            return [IsAdminUser()]

        if self.action in ["update", "partial_update"]:
            return [IsOwner()]

        return [IsAuthenticated()]



    #  3. Auto-set is_active=True when creating user


    #  4. Soft delete (DELETE → deactivate instead)
    def destroy(self, request, pk=None):
        user = self.get_object()
        user.is_active = False
        user.save()

        return Response(
            {"message": "User deactivated successfully"},
            status=status.HTTP_200_OK
        )


    #  5. Custom endpoint → /users/active/
    @action(detail=False, methods=['get'])
    def active(self, request):
        users = UserProfile.objects.filter(is_active=True)
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({"message": "User restored successfully"})
    