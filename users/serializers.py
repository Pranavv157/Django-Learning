from rest_framework import serializers
from .models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source="user.username", read_only=True)


    class Meta:
        model = UserProfile
        #fields = "__all__"
        fields = ["id","name", "email","is_active","owner"]
        #exclude=["user"]
        
        

    def create(self, validated_data):
        request = self.context.get("request")

        validated_data["user"] = request.user
        validated_data["is_active"] = True

        return super().create(validated_data)
