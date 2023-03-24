from django.shortcuts import render
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from artiste.models import Product, Artiste, Song
from .serializers import ProductSerializer, ArtisteSerializer, SongSerializer


# Create your views here.
class ArtisteView(APIView):
    serializer_class = ArtisteSerializer

    def get(self, request):
        artiste = Artiste.objects.all()
        serializer = self.serializer_class(instance=artiste, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SongView(APIView):
    serializer_class = SongSerializer

    def get(self, request):
        songs = Song.objects.all()
        serializer = self.serializer_class(instance=songs, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class productsView(APIView):
    serializer_class = ProductSerializer

    def get(self, request):
        products = Product.objects.all()
        serializer = self.serializer_class(instance=products, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    # def post(self, request):
    #     serializer = self.serializer_class(data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()
    #         return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductSongView(APIView):
    serializer_class = SongSerializer

    def get(self, request, product_id):
        product = Product.objects.filter(pk=product_id)
        songs = product.songs.all()
        serializer = self.serializer_class(instance=songs, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ProductSongDetailView(APIView):
    serializer_class = SongSerializer

    def get(self, request, product_id, song_id):
        product = Product.objects.get(pk=product_id)
        song = product.songs.filter(pk=song_id)
        serializer = self.serializer_class(instance=song)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, product_id, song_id):
        product = Product.objects.get(pk=product_id)
        song = product.songs.filter(pk=song_id)
        serializer = self.serializer_class(
            instance=song, data=request.data, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id, song_id):
        product = Product.objects.get(pk=product_id)
        song = product.songs.filter(pk=song_id)
        if song is not None:
            song.delete()
            return Response(data=[], status=status.HTTP_204_NO_CONTENT)
        return Response(
            data="Requested data does not exits", status=status.HTTP_400_BAD_REQUEST
        )


class ProductDetailView(APIView):
    serializer_class = ProductSerializer

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Http404

    def get(self, request, pk):
        product = self.get_object(pk)
        serializer = self.serializer_class(instance=product)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        product = self.get_object(pk)
        serializer = self.serializer_class(
            instance=product, data=request.data, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = self.get_object(pk)
        product.save()
        return Response(data=[], status=status.HTTP_204_NO_CONTENT)


class ArtisteProductView(APIView):
    serializer_class = ProductSerializer

    def post(self, request, artiste_id):
        artist = Artiste.objects.get(pk=artiste_id)
        product = artist.products.create(**request.data)
        serializer = self.serializer_class(product)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {"message": "product created", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, artiste_id):
        artist = Artiste.objects.get(pk=artiste_id)
        artist_products = artist.products.all()
        serializer = ProductSerializer(instance=artist_products, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
