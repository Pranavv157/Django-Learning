from django.db import models
from django.contrib.auth.models import User
class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,db_index=True)
    name = models.CharField(max_length=100,db_index=True)
    email = models.EmailField(db_index=True)
    is_active = models.BooleanField(default=True,db_index=True)



    def __str__(self):
        return self.name
