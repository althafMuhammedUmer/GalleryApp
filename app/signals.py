from django.db.models.signals import post_save
from .models import Post
from django.dispatch import receiver
from django.db.models.signals import pre_delete
import os

@receiver(pre_delete, sender=Post)
def delete_post_image(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
