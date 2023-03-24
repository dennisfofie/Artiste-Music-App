from django.db import models
from customer.models import Orders

# Create your models here.


class Artiste(models.Model):
    name = models.CharField(max_length=255)
    profile = models.ImageField(upload_to="artist/img")
    is_artist = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(decimal_places=2, max_digits=9)
    release_date = models.DateTimeField(auto_now_add=True)
    number_songs = models.IntegerField(null=True, blank=True)
    cover_img = models.ImageField(upload_to="product/img")
    artist = models.ForeignKey(
        Artiste, on_delete=models.CASCADE, related_name="products"
    )
    producer = models.CharField(max_length=150, null=True, blank=True)
    intro_video = models.FileField(upload_to="product/video")
    bio = models.TextField()
    director = models.CharField(max_length=255, null=True, blank=True)
    orders = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name="orders")

    def __str__(self):
        return self.title


class Song(models.Model):
    song_title = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="songs")
    file = models.FileField(upload_to="songs")
    cover_art = models.ImageField(upload_to="cover_art")
    description = models.TextField(max_length=1024, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    number_of_artiste = models.IntegerField(null=True, blank=True)
    length = models.IntegerField(null=True, blank=True)
    featured = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.song_title
