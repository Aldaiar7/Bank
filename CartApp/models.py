from django.db import models


class Cart(models.Model):
    STATUS_CHOICES = (
        ('not active', 1),
        ('activated', 2),
        ('expired', 3)
    )

    series = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField()
    sum = models.PositiveIntegerField()
    status = models.CharField(choices=STATUS_CHOICES, default=2, max_length=50)


class Order(models.Model):
    cart = models.ForeignKey('Cart', related_name='orders', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class OrderDetail(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    order = models.ManyToManyField('Order', related_name='order_items')
