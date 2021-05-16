from django.urls import path
from main import views

urlpatterns = [
    path('categories/', views.CategoryViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('categories/<int:pk>', views.CategoryViewSet.as_view({'get': 'retrieve', 'delete': 'destroy',
                                                               'put': 'update'})),
    path('categories/<int:pk>/item', views.ItemViewSet.as_view({'get': 'retrieve'})),
    path('items/', views.ItemViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('items/<int:pk>', views.ItemViewSet.as_view({'delete': 'destroy', 'get': 'select', 'put': 'update'})),
    path('creditcards', views.credit_card),
    path('creditcards/<int:pk>', views.CreditCardAPIView.as_view()),
    path('shoppingcart/<int:pk>', views.ShoppingCartAPIView.as_view()),
    path('shoppingcart', views.shopping_cart),
    path('orders', views.orders),
    path('orders/<int:pk>', views.OrderAPIView.as_view()),
    # path('shoppingcart/add_item/<int:pk>', views.cart_add_item)
]
