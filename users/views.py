from django.http import JsonResponse
from .models import UserProfile
from django.views.decorators.csrf import csrf_exempt

import json


# GET all users
def get_users(request):
    users = list(UserProfile.objects.values())
    return JsonResponse(users, safe=False)


@csrf_exempt
def create_user(request):

    if request.method == "POST":
        data = json.loads(request.body)

        user = UserProfile.objects.create(
            name=data["name"],
            email=data["email"]
        )

        return JsonResponse({"message": "User created", "id": user.id})


# GET single user
def get_user(request, user_id):
    user = UserProfile.objects.get(id=user_id)
    return JsonResponse({
        "id": user.id,
        "name": user.name,
        "email": user.email
    })




@csrf_exempt# DELETE user
def delete_user(request, user_id):
    UserProfile.objects.get(id=user_id).delete()
    return JsonResponse({"message": "Deleted"})

@csrf_exempt
def update_user(request, user_id):

    if request.method == "PUT":
        data = json.loads(request.body)

        user = UserProfile.objects.get(id=user_id)

        user.name = data["name"]
        user.email = data["email"]
        user.save()

        return JsonResponse({"message": "updated"})
