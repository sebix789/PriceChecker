from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=200)

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Shop(models.Model):
    name = models.CharField(max_length=200)
    
class ProductPrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    url = models.URLField()
    
class User(models.Model):
    email = models.EmailField(unique=True)
    subscribed = models.BooleanField(default=False)
