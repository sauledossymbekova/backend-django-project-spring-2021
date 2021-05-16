from django.db import models
from auth_.models import User
from utils.validators import validate_size, validate_extension


class CategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('category_name')


class Category(models.Model):
    category_name = models.CharField(max_length=100)
    objects = CategoryManager()

    class Meta:
        verbose_name = 'Категория продуктов'
        verbose_name_plural = 'Категории продуктов'

    def __str__(self):
        return self.category_name


class Manager(models.Manager):
    def get_by_category_without_relation(self, category_name):
        return self.filter(category=category_name)


class Item(models.Model):
    item_name = models.CharField(max_length=255)
    price = models.FloatField()
    description = models.CharField(max_length=255, blank=True)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, related_name='items')
    photo = models.ImageField(upload_to='item_photos',
                              validators=[validate_size, validate_extension],
                              null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.item_name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('item_name', 'price')


class CreditCard(models.Model):
    number = models.CharField(max_length=16, blank=True)
    expireDate = models.CharField(max_length=50, blank=True)
    code = models.CharField(max_length=3, blank=True)
    customer = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Кредитная карта'
        verbose_name_plural = 'Кредитные карты'

    def __str__(self):
        return self.number


class ShoppingCart(models.Model):
    cart_items = models.ManyToManyField(Item)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class Order(models.Model):
    price = models.FloatField()
    delivery_address = models.CharField(max_length=255)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    cart_items = models.ManyToManyField(ShoppingCart)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
