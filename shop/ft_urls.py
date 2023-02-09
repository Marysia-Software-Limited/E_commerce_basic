from django.urls import path
from shop.ft_views import home, products_view, categories_view, product_detail_view, category_detail_view, thanks_view
from cart.ft_views import cart_view
from orders.ft_views import order_form_view

urlpatterns = [
    path('thanks', thanks_view, name='Thank you'),
    path('order', order_form_view, name='Order'),
    path('cart', cart_view, name='Cart'),
    path('product_detail&<int:id>', product_detail_view, name='Product_details'),
    path('category_detail&<int:id>', category_detail_view, name='Category_details'),
    path('products', products_view, name='Products'),
    path('categories', categories_view, name='Categories'),
    path('', home, name='Home'),
    # path('', tasks, name="tasks"),
]
