import time

from celery import shared_task
from .models import Cart
from .models import StatusChoices


@shared_task(name='computation_heavy_task')
def computation_heavy_task(cart_id):
    cart = Cart.objects.get(id=cart_id)
    cart.status = StatusChoices.not_active
    time.sleep(5)
    cart.save()
    print(f'Running task for {cart.id} status: {cart.status}')
