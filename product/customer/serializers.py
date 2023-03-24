from rest_framework import serializers
from django.core.validators import validate_email
from customer.models import Orders, Customer, Shipment, Country


# customer serializers
class CustomerSerializer(serializers.ModelSerializer[Customer]):
    password = serializers.CharField(max_length=100, min_length=4, write_only=True)

    class Meta:
        model = Customer
        fields = "__all__"

    # def validate(self, attrs):
    #     email = validate_email(attrs.get("email"))
    #     first_name = attrs.get("firstname")
    #     last_name = attrs.get("last_name")
    #     fulname = attrs.get("fullname")

    #     if not email:
    #         raise serializers.ValidationError("Customer must have a valid email")
    #     if not first_name:
    #         raise serializers.ValidationError("Customer must have first name")
    #     if not last_name:
    #         raise serializers.ValidationError("Customer must have last name")
    #     if not fulname:
    #         raise serializers.ValidationError("Customer must have fullname")
    #     return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        customer = Customer(**validated_data)
        customer.set_password(password)
        customer.save()
        return customer

    # def update(self, instance, validated_data):
    #     password = validated_data.pop("password")
    #     for key, value in validated_data.items():
    #         setattr(instance, key, value)
    #     instance.set_password(password)
    #     instance.save()
    #     return instance


class OrdersSerializer(serializers.ModelSerializer[Orders]):
    class Meta:
        model = Orders
        fields = "__all__"


class ShipmentSerializer(serializers.ModelSerializer[Shipment]):
    class Meta:
        model = Shipment
        fields = "__all__"


class CountrySerializer(serializers.ModelSerializer[Country]):
    class Meta:
        model = Country
        fields = "__all__"
