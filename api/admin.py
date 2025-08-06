from django.contrib import admin

# Register your models here.
from .models import FitnessClass, Slot, Client, Booking
admin.site.register(FitnessClass)
admin.site.register(Slot)
admin.site.register(Client)
admin.site.register(Booking)

