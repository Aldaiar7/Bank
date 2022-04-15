from django.shortcuts import render
from rest_framework import generics, status
from rest_framework import filters
from rest_framework.response import Response

from .models import Cart
from .serializers import *


class CartListView(generics.ListAPIView):
    search_fields = ['series', 'number', 'created_at', 'expires_at', 'used_at', 'sum', 'status']
    filter_backends = (filters.SearchFilter,)
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartView(generics.ListAPIView, generics.DestroyAPIView):
    serializer_class = CartProfileSerializer

    def get_queryset(self):
        queryset = Cart.objects.filter(pk=self.kwargs['pk'])
        return queryset

    def destroy(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(args, kwargs)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer



