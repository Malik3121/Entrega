from django.shortcuts import render

# Create your views here.

# view.py
from rest_framework import viewsets, permissions
from .models import Order
from .sereliezer import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    # Определение разрешений для разных пользователей
    def get_permissions(self):
        if self.action == 'list':
            # Только администратор может видеть все заказы
            permission_classes = [permissions.IsAdminUser]
        elif self.action == 'retrieve':
            # Клиент может видеть только свои заказы, курьер может видеть только свои доставки, администратор может видеть любой заказ
            permission_classes = [permissions.IsAuthenticated, IsOrderOwnerOrCourierOrAdmin]
        elif self.action == 'create':
            # Только клиент может создавать заказ
            permission_classes = [permissions.IsAuthenticated, IsCustomer]
        elif self.action == 'update' or self.action == 'partial_update':
            # Только курьер или администратор может обновлять заказ
            permission_classes = [permissions.IsAuthenticated, IsCourierOrAdmin]
        elif self.action == 'destroy':
            # Только администратор может удалять заказ
            permission_classes = [permissions.IsAdminUser]
        else:
            # Для других действий запретить доступ
            permission_classes = [permissions.DenyAll]
        return [permission() for permission in permission_classes]