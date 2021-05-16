from rest_framework import serializers
from .models import Category, Item, CreditCard, ShoppingCart, Order


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    category_name = serializers.CharField()

    def create(self, validated_data):
        Category = Category.objects.create(category_name=validated_data.get('category_name'))
        return Category

    def update(self, instance, validated_data):
        instance.category_name = validated_data.get('category_name', instance.category_name)
        instance.save()
        return instance

    def validate(self, data):
        if data['categoryName'] == '':
            raise serializers.ValidationError("Category name should be written!")
        return data


class ItemSerializer(serializers.Serializer):
    item_name = serializers.CharField()
    price = serializers.FloatField()
    description = serializers.CharField()
    category = CategorySerializer()

    def create(self, validated_data):
        category = Category.objects.get(id=validated_data.get('category'))
        Item = Item.objects.create(item_name=validated_data.get('item_name'),
                                           price=validated_data.get('price'),
                                           description=validated_data.get('description'),
                                           category=category)
        return Item

    def update(self, instance, validated_data):
        instance.item_name = validated_data.get('item_name', instance.item_name)
        instance.price = validated_data.get('price', instance.price)
        instance.description = validated_data.get('description', instance.description)
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        return instance

    def validate(self, data):
        if data['price'] <= 0:
            raise serializers.ValidationError("Price can't be negative number or zero!")
        return data


class CreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = '__all__'

    def validate_number(self, value):
        if '-' in value:
            raise serializers.ValidationError('Invalid chars!')
        return value


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
