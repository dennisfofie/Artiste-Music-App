from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from customer.views import (
    ListCreateCustomers,
    CustomerDetailView,
    CustomerOrderDetailSpecificView,
    CustomerOrderDetailView,
    OrderDetailView,
    ListCreateOrders,
    ListCreateShipment,
    ListOrdersShipmentDetailView,
    ListAllCountryView,
    ShipmentDetailView,
    ShipmentCountryView,
    LogInView,
    LogoutView,
)

# customer endpoints

urlpatterns = [
    path("customers/", ListCreateCustomers.as_view(), name="list-create"),
    path("customers/<int:pk>/", CustomerDetailView.as_view(), name="customer-details"),
    path("orders/", ListCreateOrders.as_view(), name="orders"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="orders-detail"),
    path(
        "orders/<int:customer_id>/",
        CustomerOrderDetailView.as_view(),
        name="customer-orders",
    ),
    path(
        "orders/<int:customer_id>/<int:order_id>/",
        CustomerOrderDetailSpecificView.as_view(),
        name="customer-orders-details",
    ),
    path("shipments/", ListCreateShipment.as_view(), name="shipments"),
    path("shipments/<int:pk>/", ShipmentDetailView.as_view(), name="shipments-detail"),
    path(
        "shipments/<int:pk>/orders/<int:order_id>/",
        ListOrdersShipmentDetailView.as_view(),
        name="orders-shipment",
    ),
    path("country/", ListAllCountryView.as_view(), name="counries"),
    path(
        "shipments/<int:shipment_id>/country/<int:country_id>/",
        ShipmentCountryView.as_view(),
        name="shipment-countries",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("login/", LogInView.as_view(), name="login"),
    path("token/", TokenObtainPairView.as_view(), name="create-token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh-token"),
]
