import logging
from django.http import Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from main.models import Category, Item, CreditCard, ShoppingCart, Order
from main.serializers import CategorySerializer, ItemSerializer, CreditCardSerializer, ShoppingCartSerializer, \
    OrderSerializer
from django.shortcuts import get_object_or_404, get_list_or_404

logger = logging.getLogger(__name__)


class CategoryViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, )

    def list(self, request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Category.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = CategorySerializer(user)
        return Response(serializer.data)

    @action(methods=['POST'], detail=False, permission_classes=(IsAdminUser, ))
    def create(self, request):
        category_data = request.data
        new_category = Category.objects.create(category_name=category_data['category_name'])
        new_category.save()
        serializer = CategorySerializer(new_category)
        logger.debug(f'Category object created, ID: {serializer.instance}')
        logger.info(f'Category object created, ID: {serializer.instance}')
        return Response(serializer.data)

    def destroy(self, request, pk):
        try:
            instance = Category.objects.get(id=pk)
            instance.delete()
            logger.debug(f'Category object deleted, ID: {instance}')
            logger.info(f'Category object deleted, ID: {instance}')
        except Http404:
            logger.error(f'Category object cannot be deleted')
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['PUT'], detail=False, permission_classes=(IsAdminUser, ))
    def update(self, request, pk):
        category = Category.objects.get(id=pk)
        category.category_name = request.data['category_name']
        category.save()
        serializer = CategorySerializer(category)
        logger.debug(f'Category object updated, ID: {serializer.instance}')
        logger.info(f'Category object updated, ID: {serializer.instance}')
        return Response(serializer.data)


class ItemViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, )

    def list(self, request):
        queryset = Item.objects.all()
        serializer = ItemSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Item.objects.filter(category=pk)
        user = get_list_or_404(queryset)
        serializer = ItemSerializer(user, many=True)
        return Response(serializer.data)

    @action(methods=['POST'], detail=False, permission_classes=(IsAdminUser,))
    def create(self, request):
        item_data = request.data
        category = Category.objects.get(id=item_data['category'])
        new_item = Item.objects.create(item_name=item_data['item_name'], price=item_data['price'],
                                           description=item_data['description'], category=category)
        new_item.save()
        serializer = ItemSerializer(new_item)
        logger.debug(f'Item object created, ID: {serializer.instance}')
        logger.info(f'Item object created, ID: {serializer.instance}')
        return Response(serializer.data)

    def destroy(self, request, pk):
        try:
            instance = Item.objects.get(id=pk)
            instance.delete()
            logger.debug(f'Item object deleted, ID: {instance}')
            logger.info(f'Item object deleted, ID: {instance}')
        except Http404:
            logger.error(f'Item object cannot be deleted')
        return Response(status=status.HTTP_204_NO_CONTENT)

    def select(self, request, pk=None):
        queryset = Item.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ItemSerializer(user)
        return Response(serializer.data)

    @action(methods=['PUT'], detail=False, permission_classes=(IsAdminUser, ))
    def update(self, request, pk):
        _item = Item.objects.get(id=pk)
        _item.item_name = request.data['item_name']
        _item.price = request.data['price']
        _item.description = request.data['description']
        category = Category.objects.get(category_name=request.data['category'])
        _item.category = category
        _item.save()
        serializer = ItemSerializer(_item)
        logger.debug(f'Item object updated, ID: {serializer.instance}')
        logger.info(f'Item object updated, ID: {serializer.instance}')
        return Response(serializer.data)


@csrf_exempt
def credit_card(request):
    if request.method == 'GET':
        credit_cards = CreditCard.objects.all()
        serializer = CreditCardSerializer(credit_cards, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        json_data = JSONParser().parse(request)
        serializer = CreditCardSerializer(data=json_data)
        if serializer.is_valid():
            serializer.save()
            logger.debug(f'CreditCard object created, ID: {serializer.instance}')
            logger.info(f'CreditCard object created, ID: {serializer.instance}')
            return JsonResponse(serializer.data, safe=False)
        else:
            logger.error(f'CreditCard object is not created, ID: {serializer.errors}')
            return JsonResponse(serializer.errors, safe=False)


class CreditCardAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def get_object(self, pk):
        try:
            return CreditCard.objects.get(pk=pk)
        except CreditCard.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        card = self.get_object(pk)
        serializer = CreditCardSerializer(card, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.debug(f'CreditCard object updated, ID: {serializer.instance}')
            logger.info(f'CreditCard object updated, ID: {serializer.instance}')
            return Response(serializer.data)
        logger.error(f'CreditCard object cannot be updated, {serializer.errors}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        card = self.get_object(pk)
        card.delete()
        logger.debug(f'CreditCard object deleted')
        logger.info(f'CreditCard object deleted')
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def get_object(self, pk):
        try:
            return ShoppingCart.objects.get(customer_id=pk)
        except ShoppingCart.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        shopping_cart = self.get_object(pk)
        serializer = ShoppingCartSerializer(shopping_cart)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        shopping_cart = self.get_object(pk)
        serializer = ShoppingCartSerializer(shopping_cart, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.debug(f'ShoppingCart object updated, ID: {serializer.instance}')
            logger.info(f'ShoppingCart object updated, ID: {serializer.instance}')
            return Response(serializer.data)
        logger.error(f'ShoppingCart object cannot be updated')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        shopping_cart = self.get_object(pk)
        shopping_cart.delete()
        logger.debug(f'ShoppingCart object deleted')
        logger.info(f'ShoppingCart object deleted')
        return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
def shopping_cart(request):
    if request.method == 'POST':
        json_data = JSONParser().parse(request)
        serializer = ShoppingCartSerializer(data=json_data)
        if serializer.is_valid():
            serializer.save()
            logger.debug(f'ShoppingCart object created, ID: {serializer.instance}')
            logger.info(f'ShoppingCart object created, ID: {serializer.instance}')
            return JsonResponse(serializer.data, safe=False)
        else:
            logger.error(f'ShoppingCart object cannot be created, {serializer.errors}')
            return JsonResponse(serializer.errors, safe=False)


class OrderAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        order = self.get_object(pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        order= self.get_object(pk)
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.debug(f'Order object updated, ID: {serializer.instance}')
            logger.info(f'Order object updated, ID: {serializer.instance}')
            return Response(serializer.data)
        logger.error(f'Order object cannot be updated, {serializer.errors}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        order = self.get_object(pk)
        order.delete()
        logger.debug(f'Order object deleted')
        logger.info(f'Order object deleted')
        return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
def orders(request):
    if request.method == 'GET':
        all_orders = Order.objects.all()
        serializer = OrderSerializer(all_orders, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        json_data = JSONParser().parse(request)
        serializer = OrderSerializer(data=json_data)
        if serializer.is_valid():
            serializer.save()
            logger.debug(f'Order object created, ID: {serializer.instance}')
            logger.info(f'Order object created, ID: {serializer.instance}')
            return JsonResponse(serializer.data, safe=False)
        else:
            logger.error(f'Order object cannot be created, {serializer.errors}')
            return JsonResponse(serializer.errors, safe=False)


# def cart_add_item(request, pk):
#     cart = ShoppingCart(request)
#     item = Item.objects.get(id=pk)
#     cart.cart_items.add(item)
#     return redirect("items/")
