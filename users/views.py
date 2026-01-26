from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import UserProfile
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):

    # 1. Default queryset → only active users
    queryset = UserProfile.objects.filter(is_active=True)

    #  2. Serializer
    serializer_class = UserSerializer


    #  3. Auto-set is_active=True when creating user
    def create(self, request):
        data = request.data.copy()
        data["is_active"] = True

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        user = UserProfile.objects.get(pk=pk)
        user.is_active = True
        user.save()
        return Response({"message": "User restored successfully"})

