from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime, timedelta

class GoodTrait(models.Model):
   name = models.CharField(max_length=2000)
   description = models.CharField(max_length=8000)
   user = models.ForeignKey(User)
   image = models.ImageField(upload_to = "images", default = 'images/good_trait_default.png')

   def __str__ (self):
        return self.name

   def calc_good_for(self):
       print("id = " + str(self.id))
       checkins = GoodTraitCheckIn.objects.filter(good_trait_id=self.id).order_by('-date')
       if not checkins:
           print("no check in")
           return 0

       yesterday = datetime.today().date()

       if checkins[0].date.date() < yesterday:
        #    print("far away check ins found")
           return 0
       else:
        #    print("start the loop" + str(len(checkins)))
           prev_date = None
           good_for = 0
           for c in checkins:
               if not prev_date:
                #    print("no prev date")
                   good_for = 1
                #    print("good_for:" + str(good_for))
               else:
                   if (prev_date - c.date.date()).days > 1:
                    #    print("good_for:" + str(good_for))
                       return good_for
                   else:
                    #    print("good_for:" + str(good_for))
                       good_for = good_for + 1

               prev_date = c.date.date()
           return good_for




   def checkin(self):
       checkin = GoodTraitCheckIn(good_trait_id = self.id)
       checkin.save()
       good_for = self.calc_good_for()
       return good_for

   def rollback_checkin(self):
       checkin = GoodTraitCheckIn.objects.filter( good_trait_id = self.id, date__gte = datetime.today().date() )
       checkin.delete()
       good_for = self.calc_good_for()
       return good_for



class BadTrait(models.Model):
   name = models.CharField(max_length=2000)
   description = models.CharField(max_length=8000)
   sober_for = models.IntegerField(default=0)
   user = models.ForeignKey(User)
   image = models.ImageField(upload_to = "images", default = 'images/bad_trait_default.png')

   def actout(self):
       actout = BadTraitActOut(bad_trait_id = self.id)
       actout.save()
       sober_for = 0
       return sober_for

   def rollback_actout(self):
       actout = BadTraitActOut.objects.filter( bad_trait_id = self.id, date__gte = datetime.today().date() )
       actout.delete()
       sober_for = self.calc_sober_for()
       return sober_for

   def calc_sober_for(self):
       act_outs = BadTraitActOut.objects.filter(bad_trait_id=self.id).order_by('-date')
       if not act_outs:
           print("no check in")
           return 0
       else:
           return 1

class GoodTraitCheckIn(models.Model):
   good_trait = models.ForeignKey(GoodTrait)
   date = models.DateTimeField(default=timezone.now)

class BadTraitActOut(models.Model):
   bad_trait = models.ForeignKey(BadTrait)
   date = models.DateTimeField(default=timezone.now)
