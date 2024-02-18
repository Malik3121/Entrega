from django.db import models
                 
# Create your models here.

# models.py
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Order(models.Model):
    # Статусы доставки
    IN_TRANSIT = 'В пути'
    DELIVERED = 'Доставлен'
    NOT_PICKED_UP = 'Еще не забрали заказ'
    DELIVERY_STATUS_CHOICES = [
        (IN_TRANSIT, 'В пути'),
        (DELIVERED, 'Доставлен'),
        (NOT_PICKED_UP, 'Еще не забрали заказ'),
    ]

    # Параметры заказа
    pickup_address = models.CharField(max_length=255, verbose_name='Адрес получения заказа')
    pickup_time = models.DateTimeField(verbose_name='Желательное время получения заказа')
    delivery_address = models.CharField(max_length=255, verbose_name='Адрес доставки заказа')
    delivery_time = models.DateTimeField(verbose_name='Желательное время доставки заказа')
    contact_person = models.CharField(max_length=255, verbose_name='Контактное лицо')
    contact_number = models.CharField(max_length=20, verbose_name='Контактный номер')
    delivery_status = models.CharField(max_length=20, choices=DELIVERY_STATUS_CHOICES, default=NOT_PICKED_UP, verbose_name='Статус доставки')

    # Связи с пользователями
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='Клиент')
    courier = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='deliveries', verbose_name='Курьер')
    admin = models.ForeignKey(User, on_delete=models.PROTECT, related_name='managed_orders', verbose_name='Администратор')

    def __str__(self):
        return f'Заказ №{self.id} от {self.customer.username}'


