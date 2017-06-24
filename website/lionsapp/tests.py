from django.test import TestCase
from django.test.utils import setup_test_environment
from django.test import Client
from django.urls import reverse
from .models import *
from django.contrib.auth.models import User
from datetime import datetime, date

# Create your tests here.
class LoginTests(TestCase):

    def test_login(self):
        client = Client()
        response = client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

class GoodTraitTestCase(TestCase):
    user = None
    def setUp(self):
        self.user = User.objects.create(username='john',
                                 email='jlennon@beatles.com',
                                 password='glass onion')
        self.user.date_joined = datetime.today() + timedelta(-10)
        self.user.save()

    def test_good_trait_get_good_for(self):
        good_trait = GoodTrait.objects.create(name="strong", description="desc", user_id = self.user.id)
        good_for = good_trait.calc_good_for()
        self.assertEqual(0, good_for)

    def test_good_trait_get_good_for_1(self):
        good_trait = GoodTrait.objects.create(name="strong", description="desc", user_id = self.user.id)
        GoodTraitCheckIn.objects.create(good_trait_id=good_trait.id, date = datetime.today())
        good_for = good_trait.calc_good_for()
        self.assertEqual(1, good_for)

    def test_good_trait_get_good_for_2(self):
        good_trait = GoodTrait.objects.create(name="strong", description="desc", user_id = self.user.id)
        GoodTraitCheckIn.objects.create(good_trait_id=good_trait.id, date = datetime.today() - timedelta(-1))
        good_for = good_trait.calc_good_for()
        self.assertEqual(1, good_for)

    def test_good_trait_get_good_for_3(self):
        good_trait = GoodTrait.objects.create(name="strong", description="desc", user_id = self.user.id)
        GoodTraitCheckIn.objects.create(good_trait_id=good_trait.id, date = datetime.today())
        GoodTraitCheckIn.objects.create(good_trait_id=good_trait.id, date = datetime.today() - timedelta(1))
        good_for = good_trait.calc_good_for()
        self.assertEqual(2, good_for)

    def test_good_trait_get_good_for_4(self):
        good_trait = GoodTrait.objects.create(name="strong", description="desc", user_id = self.user.id)
        GoodTraitCheckIn.objects.create(good_trait_id=good_trait.id, date = datetime.today())
        GoodTraitCheckIn.objects.create(good_trait_id=good_trait.id, date = datetime.today() - timedelta(1))
        GoodTraitCheckIn.objects.create(good_trait_id=good_trait.id, date = datetime.today() - timedelta(2))
        good_for = good_trait.calc_good_for()
        self.assertEqual(3, good_for)

    def test_good_trait_get_good_for_4(self):
        good_trait = GoodTrait.objects.create(name="strong", description="desc", user_id = self.user.id)
        GoodTraitCheckIn.objects.create(good_trait_id=good_trait.id, date = datetime.today())
        GoodTraitCheckIn.objects.create(good_trait_id=good_trait.id, date = datetime.today() - timedelta(1))
        GoodTraitCheckIn.objects.create(good_trait_id=good_trait.id, date = datetime.today() - timedelta(3))
        good_for = good_trait.calc_good_for()
        self.assertEqual(2, good_for)

    def test_good_trait_get_good_for_5(self):
        good_trait = GoodTrait.objects.create(name="strong", description="desc", user_id = self.user.id)
        GoodTraitCheckIn.objects.create(good_trait_id=good_trait.id, date = datetime.today())
        GoodTraitCheckIn.objects.create(good_trait_id=good_trait.id, date = datetime.today() - timedelta(1))
        GoodTraitCheckIn.objects.create(good_trait_id=good_trait.id, date = datetime.today() - timedelta(2))
        GoodTraitCheckIn.objects.create(good_trait_id=good_trait.id, date = datetime.today() - timedelta(3))
        good_for = good_trait.calc_good_for()
        self.assertEqual(4, good_for)

    def test_good_trait_get_good_for_5(self):

        good_trait = GoodTrait.objects.create(name="strong", description="desc", user_id = self.user.id)
        GoodTraitCheckIn.objects.create(good_trait_id=good_trait.id, date = datetime.today())
        for i in range(100):
            GoodTraitCheckIn.objects.create(good_trait_id=good_trait.id, date = datetime.today() - timedelta(i))

        good_for = good_trait.calc_good_for()
        self.assertEqual(101, good_for)

    def test_good_trait_get_good_for_5(self):

        good_trait = GoodTrait.objects.create(name="strong", description="desc", user_id = self.user.id)
        GoodTraitCheckIn.objects.create(good_trait_id=good_trait.id, date = datetime.today() - timedelta(1) )

        good_for = good_trait.calc_good_for()
        self.assertEqual(1, good_for)

    def test_bad_trait_get_sober_for_1(self):
       bad_trait = BadTrait.objects.create(name="weak", description="desc", user_id = self.user.id)
       sober_for = bad_trait.calc_sober_for(self.user.id)
       self.assertEqual(10, sober_for)

    def test_bad_trait_get_sober_for_2(self):
       bad_trait = BadTrait.objects.create(name="weak", description="desc", user_id = self.user.id)
       BadTraitActOut.objects.create(bad_trait_id=bad_trait.id, date = datetime.today())
       sober_for = bad_trait.calc_sober_for(self.user.id)

       self.assertEqual(0, sober_for)

    def test_bad_trait_get_sober_for_3(self):
       bad_trait = BadTrait.objects.create(name="weak", description="desc", user_id = self.user.id)
       BadTraitActOut.objects.create(bad_trait_id=bad_trait.id, date = datetime.today()-timedelta(1))
       sober_for = bad_trait.calc_sober_for(self.user.id)

       self.assertEqual(1, sober_for)

    def test_bad_trait_get_sober_for_4(self):
       bad_trait = BadTrait.objects.create(name="weak", description="desc", user_id = self.user.id)
       BadTraitActOut.objects.create(bad_trait_id=bad_trait.id, date = datetime.today()-timedelta(1))
       BadTraitActOut.objects.create(bad_trait_id=bad_trait.id, date = datetime.today()-timedelta(3))
       sober_for = bad_trait.calc_sober_for(self.user.id)

       self.assertEqual(1, sober_for)
