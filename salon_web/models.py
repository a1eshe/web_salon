from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    USER_TYPES = (
        ('customer', 'Customer'),
        ('worker', 'Worker'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"
    

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=50, decimal_places=3)
    premium_price = models.DecimalField(max_digits=50, decimal_places=3, default=0)
    image = models.ImageField(upload_to='service_images/', null=True, blank=True)

    def average_price(self):
        return (self.price + self.premium_price) / 2

    def __str__(self):
        return self.name


class Employee(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    experience = models.IntegerField()  # yillarda
    bio = models.TextField()

    def __str__(self):
        return self.name
    

import string
import random

def generate_referral_code(length=6):
    characters = string.ascii_uppercase + string.digits
    while True:
        code = ''.join(random.choices(characters, k=length))
        if not Customer.objects.filter(referral_code=code).exists():
            return code

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    referral_code = models.CharField(max_length=10, unique=True, blank=True, null=True)
    discount = models.FloatField(default=0)  # Yangi mijoz uchun chegirma foizi
    referred_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        is_new = self._state.adding  # faqat yangi mijoz uchun

        if not self.referral_code:
            self.referral_code = generate_referral_code()

        super().save(*args, **kwargs)  # Dastlab self saqlanadi

    # Agar bu yangi foydalanuvchi bo'lsa va referral kodi bo'lsa
        if is_new and self.referred_by:
            self.discount = 5  # Yangi mijoz uchun chegirma

            # Referral kodi orqali keldi, referral egasiga chegirma qo‘shamiz
            referrer = self.referred_by

            # Maksimal chegirma 50% bo‘lishi kerak
            new_discount = referrer.discount + 10
            referrer.discount = min(new_discount, 50)  # 50% dan oshmasin
            referrer.save()

            # Yangi mijozni qayta saqlaymiz (chegirma bilan)
            super().save(*args, **kwargs)



PRICE_CHOICES = [
    ('Oddiy', 'Oddiy'),
    ('Premium', 'Premium'),
    ('Boshqa', 'Boshqa')
]

DISCOUNT_CHOICES = [
    ('yo\'q', 'yo\'q'),
    ('ha', 'ha')
]

class Booking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    final_price = models.DecimalField(max_digits=50, decimal_places=3, null=True, blank=True)

    price_type = models.CharField(max_length=20, choices=PRICE_CHOICES, default='Oddiy')
    discount_applied = models.CharField(max_length=5, choices=DISCOUNT_CHOICES, default='yo\'q')
 

class Review(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    sentiment = models.CharField(max_length=10, choices=[
        ('positive', 'Positive'),
        ('neutral', 'Neutral'),
        ('negative', 'Negative'),
    ], blank=True)
    def __str__(self):
        return f"{self.customer.user.username} - {self.service.name} - {self.sentiment}"

class Master(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)

    def __str__(self):
        return self.name