from django.db import models




# Создаем модель product, которая хранит информацию о продукте
class ProductSerializer(models.Model):
    # У каждого продукта есть название, описание, цена, изображение и категория
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')

    # Возвращаем название продукта при выводе объекта
    def __str__(self):
        return self.name

# Создаем модель maker, которая хранит информацию о производителе продукта
class SellerySerializer(models.Model):
    # У каждого производителя есть название, адрес, телефон и сайт
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    website = models.URLField()

    # Возвращаем название производителя при выводе объекта
    def __str__(self):
        return self.name

# Создаем модель category, которая хранит информацию о категории продукта
class CategorySerializer(models.Model):
    # У каждой категории есть название и описание
    name = models.CharField(max_length=100)
    description = models.TextField()

    # Возвращаем название категории при выводе объекта
    def __str__(self):
        return self.name
