from django.test import TestCase

# Create your tests here.

# test.py
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Order

class OrderTestCase(TestCase):
    def setUp(self):
        # Создание пользователей
        self.admin = User.objects.create_user(username='admin', password='admin', is_staff=True)
        self.customer = User.objects.create_user(username='customer', password='customer')
        self.courier = User.objects.create_user(username='courier', password='courier')

        # Создание заказа
        self.order = Order.objects.create(
            pickup_address='ул. Абая, 1',
            pickup_time='2024-02-18 14:00:00',
            delivery_address='ул. Манаса, 10',
            delivery_time='2024-02-18 15:00:00',
            contact_person='Иван Иванов',
            contact_number='+996555111222',
            customer=self.customer,
            admin=self.admin
        )

        # Создание клиента API
        self.client = APIClient()

    def test_order_list(self):
        # Тестирование списка заказов
        # Администратор может видеть все заказы
        self.client.login(username='admin', password='admin')
        response = self.client.get('/orders/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.client.logout()

        # Клиент не может видеть все заказы
        self.client.login(username='customer', password='customer')
        response = self.client.get('/orders/')
        self.assertEqual(response.status_code, 403)
        self.client.logout()

        # Курьер не может видеть все заказы
        self.client.login(username='courier', password='courier')
        response = self.client.get('/orders/')
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    def test_order_retrieve(self):
        # Тестирование получения заказа по id
        # Администратор может видеть любой заказ
        self.client.login(username='admin', password='admin')
        response = self.client.get(f'/orders/{self.order.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.order.id)
        self.client.logout()

        # Клиент может видеть только свой заказ
        self.client.login(username='customer', password='customer')
        response = self.client.get(f'/orders/{self.order.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.order.id)
        response = self.client.get(f'/orders/{self.order.id + 1}/')
        self.assertEqual(response.status_code, 404)
        self.client.logout()

        # Курьер не может видеть заказ, пока не назначен на него
        self.client.login(username='courier', password='courier')
        response = self.client.get(f'/orders/{self.order.id}/')
        self.assertEqual(response.status_code, 404)
        # Назначение курьера на заказ
        self.order.courier = self.courier
        self.order.save()
        response = self.client.get(f'/orders/{self.order.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.order.id)
        self.client.logout()

    def test_order_create(self):
        # Тестирование создания заказа
        # Клиент может создавать заказ
        self.client.login(username='customer', password='customer')
        data = {
            'pickup_address': 'ул. Чуй, 100',
            'pickup_time': '2024-02-19 10:00:00',
            'delivery_address': 'ул. Фрунзе, 50',
            'delivery_time': '2024-02-19 11:00:00',
            'contact_person': 'Петр Петров',
            'contact_number': '+996777333444',
            'customer': self.customer.id,
            'admin': self.admin.id
        }
        response = self.client.post('/orders/', data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['pickup_address'], data['pickup_address'])
        self.client.logout()

        # Администратор не может создавать заказ
        self.client.login(username='admin', password='admin')
        response = self.client.post('/orders/', data=data)
        self.assertEqual(response.status_code, 403)
        self.client.logout()

        # Курьер не может создавать заказ
        self.client.login(username='courier', password='courier')
        response = self.client.post('/orders/', data=data)
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    def test_order_update(self):
        # Тестирование обновления заказа
        # Курьер может обновлять статус доставки заказа
        self.client.login(username='courier', password='courier')
        # Назначение курьера на заказ
        self.order.courier = self.courier
        self.order.save()
        # Изменение статуса доставки на "В пути"
        data = {
            'delivery_status': Order.IN_TRANSIT
        }
        response = self.client.patch(f'/orders/{self.order.id}/', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['delivery_status'], data['delivery_status'])
        # Изменение статуса доставки на "Доставлен"
        data = {
            'delivery_status': Order.DELIVERED
        }
        response = self.client.patch(f'/orders/{self.order.id}/', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['delivery_status'], data['delivery_status'])
        self.client.logout()

        # Администратор может обновлять любой параметр заказа
        self.client.login(username='admin', password='admin')
        # Изменение адреса доставки заказа
        data = {
            'delivery_address': 'ул. Ленина, 20'
        }
        response = self.client.patch(f'/orders/{self.order.id}/', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['delivery_address'], data['delivery_address'])
        # Изменение контактного номера заказа
        data = {
            'contact_number': '+996888444555'
        }
        response = self.client.patch(f'/orders/{self.order.id}/', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['contact_number'], data['contact_number'])
        self.client.logout()

        # Клиент не может обновлять заказ
        self.client.login(username='customer', password='customer')
        # Попытка изменить адрес получения заказа
        data = {
            'pickup_address': 'ул. Советская, 5'
        }
        response = self.client.patch(f'/orders/{self.order.id}/', data=data)
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    def test_order_destroy(self):
        # Тестирование удаления заказа
        # Администратор может удалять заказ
        self.client.login(username='admin', password='admin')
        response = self.client.delete(f'/orders/{self.order.id}/')
        self.assertEqual(response.status_code, 204)
        self.client.logout()

        # Клиент не может удалять заказ
        self.client.login(username='customer', password='customer')
        response = self.client.delete(f'/orders/{self.order.id}/')
        self.assertEqual(response.status_code, 403)
        self.client.logout()

        # Курьер не может удалять заказ
        self.client.login(username='courier', password='courier')
        response = self.client.delete(f'/orders/{self.order.id}/')
        self.assertEqual(response.status_code, 403)
        self.client.logout()
