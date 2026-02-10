from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView

from django.contrib.auth.models import User
from django.core.cache import cache
from urllib.parse import urlencode

from .models import UserProfile
from .serializers import UserSerializer
from .permissions import IsOwner
from .filters import UserFilter
from .tasks import send_welcome_email

# logging
import logging
logger = logging.getLogger(__name__)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # minimal validation
        if not username or not password:
            return Response(
                {"error": "Username and password required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.create_user(username=username, password=password)
            logger.info("User created: %s", username)
        except Exception as e:
            logger.exception("Registration failed: %s", e)
            raise

        # send async email task (use stable ID instead of username)
        send_welcome_email.delay(user.id)

        return Response(
            {"message": "User created successfully"},
            status=status.HTTP_201_CREATED
        )


class UserViewSet(viewsets.ModelViewSet):

    # 1. Default queryset → only active users
    # queryset = UserProfile.objects.all()

    # optimization (no N+1 queries) + ordering for pagination safety
    queryset = (
        UserProfile.objects
        .select_related("user")
        .order_by("id")
    )

    # 2. Serializer
    serializer_class = UserSerializer

    # filtering using filtersets
    # filterset_fields = ["is_active", "name", "email","id"]

    # Advanced Filtering
    filterset_class = UserFilter

    # manual filtering
    """
    def get_queryset(self):
        queryset = self.queryset

        params = self.request.query_params
        user_id = params.get("user_id")
        name = params.get("name")
        email = params.get("email")
        is_active = params.get("is_active")

        if user_id:
            queryset = queryset.filter(id=user_id)

        if name:
            queryset = queryset.filter(name__icontains=name)

        if email:
            queryset = queryset.filter(email__icontains=email)

        if is_active is not None:
            is_active = is_active.lower() == "true"
            queryset = queryset.filter(is_active=is_active)

        return queryset
    """

    # Ordering
    # ordering_fields = ["id", "name", "email"]
    # ordering = ["id"]   # default order

    # Redis caching + pagination safe
    def list(self, request, *args, **kwargs):

        params = urlencode(sorted(request.query_params.items()))
        cache_key = f"users:{request.user.id}:{params}"

        cached = cache.get(cache_key)
        if cached:
            logger.info("Users list cache hit")
            return Response(cached)

        logger.info("Users list cache miss")

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60)

        return response

    def get_permissions(self):

        if self.action == "destroy":
            return [IsAdminUser()]

        if self.action in ["update", "partial_update"]:
            return [IsAuthenticated(), IsOwner()]

        return [IsAuthenticated()]

    # 4. Soft delete (DELETE → deactivate instead)
    def destroy(self, request, pk=None):
        user = self.get_object()
        user.is_active = False
        user.save(update_fields=["is_active"])

        cache.clear()

        return Response(
            {"message": "User deactivated successfully"},
            status=status.HTTP_200_OK
        )

    # 5. Custom endpoint → /users/active/
    @action(detail=False, methods=['get'])
    def active(self, request):
        users = (
            UserProfile.objects
            .select_related("user")
            .filter(is_active=True)
            .order_by("id")
        )

        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        user = self.get_object()
        user.is_active = True
        user.save(update_fields=["is_active"])

        cache.clear()

        return Response({"message": "User restored successfully"})
