from django.urls import path
from .views import (
    ArtisteView,
    SongView,
    productsView,
    ProductSongView,
    ProductSongDetailView,
    ProductDetailView,
    ArtisteProductView,
)


urlpatterns = [
    path("artiste/", ArtisteView.as_view(), name="list artiste"),
    path("songs/", SongView.as_view(), name="songs"),
    path("products/", productsView.as_view(), name="products"),
    path("products/songs/", ProductSongView.as_view(), name="product-songs"),
    path(
        "products/<int:product_id>/songs/<int:song_id>/",
        ProductSongDetailView.as_view(),
        name="product-song-detail",
    ),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product-details"),
    path(
        "artiste/<int:artiste_id>/", ArtisteProductView.as_view(), name="artiste-detail"
    ),
]
