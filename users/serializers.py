from rest_framework import serializers
from .models import UserProfile


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = "__all__"
        read_only_fields = ["user", "is_active"]


    def create(self, validated_data):
        request = self.context.get("request")

        validated_data["user"] = request.user
        validated_data["is_active"] = True

        return super().create(validated_data)
