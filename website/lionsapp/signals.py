from .models import Resource
from django.db.models.signals import post_save
from django.dispatch import receiver

# @receiver(post_save, sender=Resource)
# def index_post(sender, instance, **kwargs):
    # print("indexing");
    # instance.indexing()
