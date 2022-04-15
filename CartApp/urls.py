from .views import *
from django.urls import path

urlpatterns = [
    path('carts/', CartListView.as_view()),
    path('cart/<int:pk>/', CartView.as_view()),
    path('order/', OrderListCreateView.as_view()),
    path('cart/<int:pk>/status/', CartUpdateView.as_view())
]
