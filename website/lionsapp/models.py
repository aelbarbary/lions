from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Habbit(models.Model):
   name = models.CharField(max_length=2000)
   is_good = models.BooleanField(default=False)
   user = models.ForeignKey(User)
   is_done = models.BooleanField(default=False)
   last_done = models.DateField(default=timezone.now)
   image = models.ImageField(upload_to = "images", default = 'images/good_habbit.png')

class HabbitCheckIn(models.Model):
   habbit = models.ForeignKey(Habbit)
   check_in_date = models.DateField(default=timezone.now)
