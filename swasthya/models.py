from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

typeCat=(
    ("Doctor", "Doctor"),
    ("Patient","Patient")
)

class account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    acctype = models.CharField(max_length=15,choices=typeCat, blank=False, null=False)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        account.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.account.save()
