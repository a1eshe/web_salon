from django.contrib import admin
from .models import Service, Employee, Booking, Customer, Review, Master,Profile

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'referral_code', 'referred_by', 'discount']


admin.site.register(Service)
admin.site.register(Employee)
admin.site.register(Booking)
admin.site.register(Customer)
admin.site.register(Review)
admin.site.register(Master)
admin.site.register(Profile)

