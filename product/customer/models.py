from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
import pycountry

# Create your models here.

LANGUAGE_CHOICES = [
    ("en", "English"),
    ("es", "Spanish"),
    ("fr", "French"),
    ("de", "German"),
    ("zh", "Chinese"),
    ("ar", "Arabic"),
    ("hi", "Hindi"),
    ("pt", "Portuguese"),
    ("ru", "Russian"),
    ("ja", "Japanese"),
    ("bn", "Bengali"),
    ("jv", "Javanese"),
    ("ko", "Korean"),
    ("vi", "Vietnamese"),
    ("tr", "Turkish"),
    ("it", "Italian"),
    ("pl", "Polish"),
    ("uk", "Ukrainian"),
    ("ro", "Romanian"),
    ("nl", "Dutch"),
    ("el", "Greek"),
    ("hu", "Hungarian"),
    ("cs", "Czech"),
    ("sv", "Swedish"),
    ("fi", "Finnish"),
    ("ca", "Catalan"),
    ("no", "Norwegian"),
    ("he", "Hebrew"),
    ("sr", "Serbian"),
    ("da", "Danish"),
    ("hr", "Croatian"),
    ("bg", "Bulgarian"),
    ("sw", "Swahili"),
    ("yo", "Yoruba"),
]

genre_choices = [
    ("ROCK", "Rock"),
    ("POP", "Pop"),
    ("HIP_HOP", "Hip hop"),
    ("JAZZ", "Jazz"),
    ("CLASSICAL", "Classical"),
    ("ELECTRONIC", "Electronic"),
    ("COUNTRY", "Country"),
    ("FOLK", "Folk"),
    ("R_B", "R&B"),
    ("BLUES", "Blues"),
    ("REGGAE", "Reggae"),
    ("WORLD", "World"),
    ("METAL", "Metal"),
    ("PUNK", "Punk"),
    ("INDIE", "Indie"),
]


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        user = self.model(
            username=username, email=self.normalize_email(email), **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email=email, **extra_fields)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class Customer(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, db_index=True)
    username = models.CharField(max_length=255, unique=True, db_index=True)
    first_name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    profile_pic = models.ImageField(upload_to="img", blank=True, null=True)
    phone_number = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=150, choices=LANGUAGE_CHOICES)
    bio = models.TextField(null=True, blank=True)
    prefferd_genre = models.CharField(
        max_length=50, choices=genre_choices, blank=True, null=True
    )
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    objects = CustomUserManager()

    class Meta:
        ordering = ["first_name"]

    def __str__(self) -> str:
        return self.full_name


Country_choices = [(country.alpha_2, country.name) for country in pycountry.countries]
Country_choices.sort(key=lambda x: x[1])


continent_choices = [
    ("AF", "Africa"),
    ("AN", "Antarctica"),
    ("AS", "Asia"),
    ("EU", "Europe"),
    ("NA", "North America"),
    ("OC", "Oceania"),
    ("SA", "South America"),
]


class Country(models.Model):
    name = models.CharField(
        max_length=100, null=True, blank=True, choices=Country_choices
    )
    state = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    zipcode = models.CharField(max_length=100, null=True, blank=True)
    continent = models.CharField(
        max_length=100, null=True, blank=True, choices=continent_choices
    )

    def __str__(self):
        return self.name


class Shipment(models.Model):
    receiver_address = models.CharField(max_length=100)
    receiver_address_1 = models.CharField(max_length=100, null=True, blank=True)
    receiver_address_2 = models.CharField(max_length=100, blank=True, null=True)
    country = models.OneToOneField(
        Country, on_delete=models.CASCADE, related_name="shipments"
    )

    def __str__(self):
        return str(self.country)


class Orders(models.Model):
    order_date = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="orders"
    )
    Shipment = models.OneToOneField(
        Shipment, on_delete=models.CASCADE, related_name="orders"
    )

    def __str__(self):
        return str(self.order_date)
