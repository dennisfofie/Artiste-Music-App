from django.contrib import admin
from .models import Artiste, Song, Product

# Register your models here.
admin.site.register(Artiste)
admin.site.register(Song)
admin.site.register(Product)
