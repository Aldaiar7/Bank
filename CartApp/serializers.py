from rest_framework import serializers
from .models import *


class OrderDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderDetail
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderDetailSerializer

    class Meta:
        model = Order
        fields = ['id', 'cart', 'created_at', 'order_items']


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = '__all__'


class CartProfileSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'series', 'number', 'orders']


class CartGeneratorSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(write_only=True)

    class Meta:
        model = Cart
        fields = '__all__'


class CartStatusSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = Cart
        fields = ['id', 'status']
