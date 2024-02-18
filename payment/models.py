# models.py
from django.db import models
from account.models import CustomUser
class Payment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='payments')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)