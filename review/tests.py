from django.test import TestCase

# Create your tests here.
# reviews/test.py
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Review
from .serializers import ReviewSerializer

@pytest.fixture
def api_client():
    # Создаем клиент для тестирования API
    return APIClient()

@pytest.fixture
def user():
    # Создаем тестового пользователя
    return User.objects.create_user(username="testuser", password="testpass")

@pytest.fixture
def courier():
    # Создаем тестового курьера
    return User.objects.create_user(username="testcourier", password="testpass")

@pytest.fixture
def review(courier, user):
    # Создаем тестовый отзыв
    return Review.objects.create(rating=5, comment="Good service", courier=courier, client=user)

def test_review_model(review):
    # Тестируем модель Review
    assert review.rating == 5
    assert review.comment == "Good service"
    assert str(review) == "5 stars from testuser to testcourier"

def test_review_serializer(review):
    # Тестируем сериализатор ReviewSerializer
    serializer = ReviewSerializer(review)
    data = serializer.data
    assert data["id"] == review.id
    assert data["rating"] == review.rating
    assert data["comment"] == review.comment
    assert data["courier"] == review.courier.id
    assert data["client"] == review.client.id
    assert data["created"] == review.created.isoformat()

def test_review_viewset_get_all(api_client, review):
    # Тестируем представление ReviewViewSet для получения всех отзывов
    response = api_client.get("/reviews/")
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["id"] == review.id

def test_review_viewset_get_single(api_client, review):
    # Тестируем представление ReviewViewSet для получения одного отзыва
    response = api_client.get(f"/reviews/{review.id}/")
    assert response.status_code == 200
    assert response.data["id"] == review.id

def test_review_viewset_post(api_client, courier, user):
    # Тестируем представление ReviewViewSet для создания отзыва
    api_client.login(username="testuser", password="testpass") # Авторизуемся как клиент
    data = {"rating": 4, "comment": "Fast delivery", "courier": courier.id} # Данные для создания отзыва
    response = api_client.post("/reviews/", data, format="json") # Отправляем POST-запрос
    assert response.status_code == 201 # Проверяем статус-код
    assert response.data["rating"] == 4 # Проверяем данные в ответе
    assert response.data["comment"] == "Fast delivery"
    assert response.data["courier"] == courier.id
    assert response.data["client"] == user.id
    assert Review.objects.count() == 2 # Проверяем, что отзыв создан в базе данных

def test_review_viewset_put(api_client, review):
    # Тестируем представление ReviewViewSet для обновления отзыва
    api_client.login(username="testuser", password="testpass") # Авторизуемся как клиент
    data = {"rating": 3, "comment": "Average service"} # Данные для обновления отзыва
    response = api_client.put(f"/reviews/{review.id}/", data, format="json") # Отправляем PUT-запрос
    assert response.status_code == 200 # Проверяем статус-код
    assert response.data["rating"] == 3 # Проверяем данные в ответе
    assert response.data["comment"] == "Average service"
    review.refresh_from_db() # Обновляем данные из базы данных
    assert review.rating == 3 # Проверяем, что отзыв обновлен в базе данных
    assert review.comment == "Average service"

def test_review_viewset_delete(api_client, review):
    # Тестируем представление ReviewViewSet для удаления отзыва
    api_client.login(username="testuser", password="testpass") # Авторизуемся как клиент
    response = api_client.delete(f"/reviews/{review.id}/") # Отправляем DELETE-запрос
    assert response.status_code == 204 # Проверяем статус-код
    assert Review.objects.count() == 0 # Проверяем, что отзыв удален из базы данных
