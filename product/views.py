from rest_framework import generics
from .models import Product, Seller, Category
from .serializer import ProductSerializer, SellerySerializer, CategorySerializer

# Создаем представление для списка всех продуктов
class ProductList(generics.ListAPIView):
    # Указываем, что источником данных будет модель Product
    queryset = Product.objects.all()
    # Указываем, что сериализатором будет ProductSerializer
    serializer_class = ProductSerializer

# Создаем представление для деталей одного продукта
class ProductDetail(generics.RetrieveAPIView):
    # Указываем, что источником данных будет модель Product
    queryset = Product.objects.all()
    # Указываем, что сериализатором будет ProductSerializer
    serializer_class = ProductSerializer

# Создаем представление для списка всех производителей
class MakerList(generics.ListAPIView):
    # Указываем, что источником данных будет модель Maker
    queryset = Seller.objects.all()
    # Указываем, что сериализатором будет MakerSerializer
    serializer_class = SellerySerializer

# Создаем представление для деталей одного производителя
class MakerDetail(generics.RetrieveAPIView):
    # Указываем, что источником данных будет модель Maker
    queryset = Seller.objects.all()
    # Указываем, что сериализатором будет MakerSerializer
    serializer_class = SellerySerializer
    
# Создаем представление для списка всех категорий
class CategoryList(generics.ListAPIView):
    # Указываем, что источником данных будет модель Category
    queryset = Category.objects.all()
    # Указываем, что сериализатором будет CategorySerializer
    serializer_class = CategorySerializer

# Создаем представление для деталей одной категории
class CategoryDetail(generics.RetrieveAPIView):
    # Указываем, что источником данных будет модель Category
    queryset = Category.objects.all()
    # Указываем, что сериализатором будет CategorySerializer
    serializer_class = CategorySerializer

