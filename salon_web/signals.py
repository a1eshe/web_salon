from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Customer
import random
import string
# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, user_type='customer')  # default 'customer'

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

def generate_referral_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

@receiver(post_save, sender=Customer)
def create_referral_code(sender, instance, created, **kwargs):
    if created and not instance.referral_code:
        instance.referral_code = generate_referral_code()
        instance.save()
