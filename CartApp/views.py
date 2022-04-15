from django.shortcuts import render
from rest_framework import generics
from rest_framework import filters
from .models import Cart
from .serializers import *


class CartListView(generics.ListAPIView):
    search_fields = ['series', 'number', 'created_at', 'expires_at', 'used_at', 'sum', 'status']
    filter_backends = (filters.SearchFilter,)
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartView(generics.ListAPIView):
    serializer_class = CartProfileSerializer

    def get_queryset(self):
        queryset = Cart.objects.filter(pk=self.kwargs['pk'])
        return queryset


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
