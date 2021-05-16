from django.contrib import admin
from .models import Category, Item, CreditCard, Order, ShoppingCart

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(CreditCard)
admin.site.register(ShoppingCart)
admin.site.register(Order)
