from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Club(models.Model):
    club_name = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=5)
    city = models.CharField(max_length=100)  
    date = models.DateField(default=timezone.now)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.club_name}'