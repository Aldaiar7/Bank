import time

from celery import shared_task
from .models import Cart


@shared_task(name='computation_heavy_task')
def computation_heavy_task(cart_id):
    cart = Cart.objects.get(id=cart_id)
    cart.status = '2'
    time.sleep(5)
    cart.save()
    print(f'Running task for {cart.id} status: {cart.status}')
