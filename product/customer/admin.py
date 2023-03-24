from django.contrib import admin
from .models import Shipment, Orders, Customer, Country

# Register your models here.
admin.site.register(Country)
admin.site.register(Shipment)
admin.site.register(Orders)
admin.site.register(Customer)
