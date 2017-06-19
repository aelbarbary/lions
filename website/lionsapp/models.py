from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Habbit(models.Model):
   name = models.CharField(max_length=2000)
   description = models.CharField(max_length=8000)
   is_good = models.BooleanField(default=False)
   user = models.ForeignKey(User)
   image = models.ImageField(upload_to = "images", default = 'images/good_habbit.png')

class HabbitCheckIn(models.Model):
   habbit = models.ForeignKey(Habbit)
   check_in_date = models.DateTimeField(default=timezone.now)
