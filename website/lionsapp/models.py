from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from dateutil import tz
import pytz

class GoodTrait(models.Model):
   name = models.CharField(max_length=2000)
   description = models.CharField(max_length=8000)
   user = models.ForeignKey(User)
   image = models.ImageField(upload_to = "images", default = 'images/good_trait_default.png')

   def __str__ (self):
        return self.name

   def is_checked_in_today(self):
       checkins = GoodTraitCheckIn.objects.filter( good_trait_id= self.id).order_by('-date')[:1]
       if len(checkins) > 0:
           last_check_in = timezone.localtime(checkins[0].date, pytz.timezone('US/Pacific'))
           if last_check_in.date() == datetime.now().date():
               return True
           else:
               return False
       else:
           return False

   def calc_good_for(self):
       checkins = GoodTraitCheckIn.objects.filter(good_trait_id=self.id).order_by('-date')
       if not checkins:
           return 0

       yesterday = datetime.today().date() - timedelta(1)
       last_check_in = timezone.localtime(checkins[0].date, pytz.timezone('US/Pacific'))

       if last_check_in.date() < yesterday:
           return 0
       else:
           prev_date = None
           good_for = 0
           for c in checkins:
               if not prev_date:
                   good_for = 1
               else:
                   if (prev_date - c.date.date()).days > 1:
                       return good_for
                   else:
                       good_for = good_for + 1

               prev_date = c.date.date()
           return good_for

   def checkin(self):
       checkin = GoodTraitCheckIn(good_trait_id = self.id)
       checkin.save()
       good_for = self.good_for + 1
       return good_for

   def rollback_checkin(self):
       checkin = GoodTraitCheckIn.objects.filter( good_trait_id = self.id, date__gte = datetime.today().date() )
       checkin.delete()
       good_for = self.calc_good_for()
       return good_for

class GoodTraitCheckIn(models.Model):
   good_trait = models.ForeignKey(GoodTrait)
   date = models.DateTimeField(default=timezone.now)
   def __str__ (self):
       return self.good_trait.name + " : " +  str(timezone.localtime(self.date, pytz.timezone('US/Pacific')))


class BadTrait(models.Model):
   name = models.CharField(max_length=2000)
   description = models.CharField(max_length=8000)
   sober_for = models.IntegerField(default=0)
   user = models.ForeignKey(User)
   image = models.ImageField(upload_to = "images", default = 'images/bad_trait_default.png')

   def __str__ (self):
        return self.name

   def actout(self, user_id):
       actout = BadTraitActOut(bad_trait_id = self.id)
       actout.save()
       sober_for = self.calc_sober_for(user_id)
       return sober_for

   def rollback_actout(self, user_id):
       actout = BadTraitActOut.objects.filter( bad_trait_id = self.id, date__gte = datetime.today().date() )
       actout.delete()
       sober_for = self.calc_sober_for(user_id)
       return sober_for

   def is_acted_out_today(self, user):
       act_out_list = BadTraitActOut.objects.filter( bad_trait_id= self.id).order_by('-date')[:1]
       if act_out_list:
           last_act_out = timezone.localtime(act_out_list[0].date, pytz.timezone('US/Pacific'))
           today = datetime.today().date()
           if  last_act_out.date() == today:
               return True
       return False

   def calc_sober_for(self, user_id):
       from_zone = tz.gettz('UTC')
       to_zone = tz.gettz('PST')

       act_outs = BadTraitActOut.objects.filter(bad_trait_id=self.id).order_by('-date')
       today = datetime.today().date()
       if not act_outs:
           print("no check in")
           user = User.objects.get(pk = user_id)
           delta = (today - user.date_joined.date() ).days
           return delta
       else:
           last_act_out = timezone.localtime(act_outs[0].date, pytz.timezone('US/Pacific'))
           print("last_act_out:" + str(last_act_out))
           delta = (today - last_act_out.date()).days
           return delta


class BadTraitActOut(models.Model):
   bad_trait = models.ForeignKey(BadTrait)
   date = models.DateTimeField(default=timezone.now)

   def __str__ (self):
        return self.bad_trait.name + " : " +  str(timezone.localtime(self.date, pytz.timezone('US/Pacific')))

class DateConverter(models.Model):
    def convert_utc_to_local(date):
        UTC_OFFSET_TIMEDELTA = datetime.utcnow() - datetime.now()
        print("delta: " + str(UTC_OFFSET_TIMEDELTA))
        date = date - timedelta()
        return date
