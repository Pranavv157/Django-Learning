from django.db import models
from django.contrib.auth.models import User
class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)



    def __str__(self):
        return self.name
