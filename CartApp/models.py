import json
from django.utils import timezone
from enum import Enum

from django.db import models
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from enumchoicefield import EnumChoiceField


class StatusChoices(Enum):
    active = 'active'
    not_active = 'not active'
    expired = 'expired'


class ExpiresChoices(Enum):
    year = '365 days'
    half_year = '182 days'
    month = '30 days'
    one_min = '1 min'


class Cart(models.Model):
    series = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = EnumChoiceField(ExpiresChoices, default=ExpiresChoices.year)
    used_at = models.DateTimeField()
    sum = models.PositiveIntegerField()
    status = EnumChoiceField(StatusChoices, default=StatusChoices.active)
    task = models.OneToOneField(PeriodicTask, on_delete=models.CASCADE, null=True, blank=True)

    def cart_task(self):
        self.task = PeriodicTask.objects.create(
            name=self.series,
            task='computation_heavy_task',
            interval=self.interval_schedule,
            args=json.dumps([self.id]),
            start_time=timezone.now()
        )
        print(self.task.args)
        self.save()

    @property
    def interval_schedule(self):
        if self.expires_at == ExpiresChoices.one_min:
            return IntervalSchedule.objects.get(every=1, period='minutes')
        if self.expires_at == ExpiresChoices.year:
            return IntervalSchedule.objects.get(every=365, period='days')
        if self.expires_at == ExpiresChoices.month:
            return IntervalSchedule.objects.get(every=30, period='days')
        if self.expires_at == ExpiresChoices.half_year:
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
