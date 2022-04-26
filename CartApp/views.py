import json

from django.shortcuts import render
from rest_framework import generics, status
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Cart
from .serializers import *
import datetime


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


class GeneratorCartsView(generics.CreateAPIView):

    serializer_class = CartGeneratorSerializer

    def create(self, request, *args, **kwargs):
        quantity = request.data.get('quantity')
        expires_at = request.data.get('expires_at')
        series = request.data.get('series')
        number = request.data.get('number')
        status_cart = request.data.get('status')
        sum = request.data.get('sum')
        used_at = request.data.get('used_at')

        for _ in range(int(quantity)):
            cart = Cart.objects.create(expires_at=expires_at, series=series,
                                       number=number, status=status_cart, sum=sum, used_at=used_at)
            cart.save()

        return Response('suka python govno', status=status.HTTP_201_CREATED)


class ChangeStatusView(generics.UpdateAPIView):
    serializer_class = CartStatusSerializer
    queryset = Cart.objects.all()

    def update(self, request, *args, **kwargs):
        queryset = Cart.objects.get(pk=request.data.get('id'))
        queryset.status = request.data.get('status')
        queryset.save()

        return Response({'id': queryset.id, 'status': queryset.status}, status=status.HTTP_200_OK)

