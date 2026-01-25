from django.urls import path
from . import views

"""urlpatterns = [
    path('', views.get_users),
    path('create/', views.create_user),
    path('<int:user_id>/', views.get_user),
    path('<int:user_id>/delete/', views.delete_user),
    path('<int:user_id>/update/', views.update_user),
]"""

from django.urls import path
from .views import UserList, UserDetail

urlpatterns = [
    path('', UserList.as_view()),
    path('<int:pk>/', UserDetail.as_view()),
]
