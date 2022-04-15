from django.contrib import admin
from .models import *


class OrderDetailInline(admin.StackedInline):
    model = OrderDetail.order.through


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderDetailInline]


admin.site.register(Cart)
admin.site.register(Order, OrderAdmin)

