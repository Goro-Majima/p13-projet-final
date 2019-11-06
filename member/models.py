from django.db import models
from user.models import Club

class Member(models.Model):
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    birth = models.DateField()
    street_adress = models.CharField(max_length=100)
    email = models.EmailField(max_length=70, blank=True)
    certificate = models.BooleanField(default=False)
    payment = models.BooleanField(default=False)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.last_name, self.first_name}'