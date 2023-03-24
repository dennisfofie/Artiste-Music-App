from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from customer.models import Customer, Orders, Shipment, Country
from django.contrib.auth.mixins import LoginRequiredMixin
from customer.serializers import (
    CustomerSerializer,
    OrdersSerializer,
    ShipmentSerializer,
    CountrySerializer,
)
from django.contrib.auth import authenticate, login
from customer.token import generate_token

# Create your views here.


class LogInView(APIView):
    serializer_class = CustomerSerializer

    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            tokens = generate_token(user)
            response = {"message": "Login successfully", "tokens": tokens}
            return Response(data=response, status=status.HTTP_200_OK)
        return Response(data="Invalid credentials, try again")


class LogoutView(APIView):
    serializer_class = CustomerSerializer

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            refresh = RefreshToken(refresh_token)
            refresh.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ListCreateCustomers(APIView):
    serializer_class = CustomerSerializer

    def get(self, request):
        customer = Customer.objects.all()
        serializer = self.serializer_class(instance=customer, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerDetailView(APIView):
    serializer_class = CustomerSerializer

    def get_object(self, pk):
        try:
            return Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            Http404

    def get(self, request, pk):
        customer = self.get_object(pk)
        serializer = self.serializer_class(instance=customer)
        if serializer is not None:
            return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        customer = self.get_object(pk)
        serializer = self.serializer_class(
            data=request.data, instance=customer, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response = {"message": "Data have been updated", "data": serializer.data}
            return Response(data=response, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        customer = self.get_object(pk)
        customer.delete()
        return Response(
            data={
                "data": [],
            },
            status=status.HTTP_204_NO_CONTENT,
        )


class ListCreateOrders(APIView):
    serializer_class = OrdersSerializer

    def get(self, request):
        orders = Orders.objects.all()
        serializer = self.serializer_class(instance=orders, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                data={"message": "order created", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(APIView):
    serializer_class = OrdersSerializer

    def get_objects(self, pk):
        try:
            return Orders.objects.get(pk=pk)
        except Orders.DoesNotExist:
            Http404

    def get(self, request, pk):
        order = self.get_objects(pk)

        serialiazer = self.serializer_class(instance=order)
        return Response(data=serialiazer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        order = self.get_objects(pk)

        serializer = self.serializer_class(
            instance=order, data=request.data, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(data=serializer.errors)

    def delete(self, request, pk):
        order = self.get_objects(pk)

        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomerOrderDetailView(APIView):
    serializer_class = OrdersSerializer

    def get(self, request, customer_id):
        customer = Customer.objects.get(pk=customer_id)
        orders = customer.orders.all()

        serializer = self.serializer_class(instance=orders, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CustomerOrderDetailSpecificView(APIView):
    serializer_class = OrdersSerializer

    def get(self, request, customer_id, order_id):
        customer = Customer.objects.get(pk=customer_id)
        order = customer.orders.filter(pk=order_id)
        serializer = self.serializer_class(instance=order)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, customer_id, order_id):
        customer = Customer.objects.get(pk=customer_id)
        order = customer.orders.filter(pk=order_id)
        serializer = self.serializer_class(
            instance=order, data=request.data, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, customer_id, order_id):
        customer = Customer.objects.get(pk=customer_id)
        order = customer.orders.filter(pk=order_id)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListCreateShipment(APIView):
    serializer_class = ShipmentSerializer

    def get(self, request):
        shipments = Shipment.objects.all()
        serilizer = self.serializer_class(instance=shipments, many=True)
        return Response(data=serilizer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.errors)


class ShipmentDetailView(APIView):
    serializer_class = ShipmentSerializer

    def get_objects(self, pk):
        try:
            return Shipment.objects.all(pk=pk)
        except Shipment.DoesNotExist:
            return Http404

    def get(self, request, pk):
        shipment = self.get_objects(pk)
        serializer = self.serializer_class(instance=shipment)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        shipment = self.get_objects(pk)
        serializer = self.serializer_class(
            data=request.data, instance=shipment, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        shipment = self.get_objects(pk)
        shipment.delete()
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ListOrdersShipmentDetailView(APIView):
    serializer_class = ShipmentSerializer

    def get(self, request, shipment_id, order_id):
        shipment = Shipment.objects.get(pk=shipment_id)
        order_with_this_id = shipment.orders.filter(pk=order_id)
        serializer = ShipmentSerializer(instance=order_with_this_id)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, shipment_id, order_id):
        shipment = Shipment.objects.get(pk=shipment_id)
        orders = shipment.orders.get(pk=order_id)
        serializer = self.serializer_class(
            data=request.data, instance=orders, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(data=serializer.errors)

    def delete(self, request, shipment_id, order_id):
        shipment = Shipment.objects.get(pk=shipment_id)
        order = shipment.orders.get(pk=order_id)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListAllCountryView(APIView):
    serializer_class = Country

    def get(self, request):
        coutries = Country.objects.all()
        serializer = self.serializer_class(instance=coutries, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ShipmentCountryView(APIView):
    serializer_class = Country

    def get(self, request, shipment_id, country_id):
        shipment = Shipment.objects.get(pk=shipment_id)
        country = shipment.shipments.filter(pk=country_id)

        serializer = self.serializer_class(instance=country)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, shipment_id, country_id):
        shipment = Shipment.objects.get(pk=shipment_id)
        country = shipment.shipments.filter(pk=country_id)

        serializer = self.serializer_class(
            data=request.data, instance=country, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, shipment_id, country_id):
        shipment = Shipment.objects.get(pk=shipment_id)
        country = shipment.shipments.filter(pk=country_id)
        country.delete()
        return Response(data=[], status=status.HTTP_204_NO_CONTENT)
