from django.urls import path
from shop.ft_views import home, products_view, categories_view

urlpatterns = [
    path('/products', products_view),
    path('/categories', categories_view),
    path('/', home),
    # path('', tasks, name="tasks"),
]
