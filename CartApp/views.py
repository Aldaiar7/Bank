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


class CartUpdateView(generics.UpdateAPIView):
    def get_queryset(self):
        queryset = Cart.objects.filter(pk=self.kwargs['pk'])
        return queryset
    serializer_class = CartSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'status updated successfully'})
        else:
            return Response({'message': 'failed', 'details': serializer.errors})
