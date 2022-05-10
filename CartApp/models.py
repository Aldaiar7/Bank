import json
from django.utils import timezone
from django.db import models
from django_celery_beat.models import PeriodicTask, IntervalSchedule


class Cart(models.Model):
    StatusChoices = (
        ('1', 'active'),
        ('2', 'not active'),
        ('3', 'expired')
    )

    ExpiresChoices = (
        ('365 days', 'year'),
        ('182 days', 'half_year'),
        ('30 days', 'month'),
        ('min', '1 min')
        )

    series = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.CharField(max_length=20, choices=ExpiresChoices, default='1 min')
    used_at = models.DateTimeField()
    sum = models.PositiveIntegerField()
    status = models.CharField(choices=StatusChoices, max_length=20, default='1')
    task = models.OneToOneField(PeriodicTask, on_delete=models.CASCADE, null=True, blank=True)

    def cart_task(self):
        self.task = PeriodicTask.objects.create(
            name=self.series + str(self.id),
            task='computation_heavy_task',
            interval=self.interval_schedule,
            args=json.dumps([self.id]),
            start_time=timezone.now(),
            one_off=True
        )
        print(self.task.args)
        self.save()

    @property
    def interval_schedule(self):
        if self.expires_at == 'min':
            return IntervalSchedule.objects.get(every=1, period='minutes')
        if self.expires_at == '365 days':
            return IntervalSchedule.objects.get(every=365, period='days')
        if self.expires_at == '30 days':
            return IntervalSchedule.objects.get(every=30, period='days')
        if self.expires_at == '182 days':
            return IntervalSchedule.objects.get(evey=182, period='days')

        raise NotImplementedError

    def delete(self, *args, **kwargs):
        if self.task is not None:
            self.task.delete()
        return super(self.__class__, self).delete(*args, **kwargs)


class Order(models.Model):
    cart = models.ForeignKey('Cart', related_name='orders', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class OrderDetail(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    order = models.ManyToManyField('Order', related_name='order_items')
