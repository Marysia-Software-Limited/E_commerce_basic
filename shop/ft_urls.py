from django.urls import path
from shop.ft_views import home, products_view, categories_view, product_detail_view, category_detail_view

urlpatterns = [
    path('product_detail&<int:id>', product_detail_view, name='Product_details'),
    path('category_detail&<int:id>', category_detail_view, name='Category_details'),
    path('products', products_view, name='Products'),
    path('categories', categories_view, name='Categories'),
    path('', home, name='Home'),
    # path('', tasks, name="tasks"),
]
