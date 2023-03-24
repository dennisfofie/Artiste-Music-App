from rest_framework import serializers
from artiste.models import Product, Artiste, Song


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ArtisteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artiste
        fields = "__all__"


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = "__all__"
