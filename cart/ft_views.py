import flet as ft

from django.shortcuts import get_object_or_404
from shop.models import Product
from .cart import Cart


def cart_add(page, product_id):
    """
    Receive product ID as a parameter and
    retrieve the Product instance with given ID;
    Validate CartAddProductForm - if valid,
    add or update item in the cart and redirect
    to the cart_detail URL to display cart contents.
    :param request: required parameter for any view
    :param product_id: passing product id value
    :return: redirect to the cart_detail page.
    """
    cart = Cart(page)
    product = get_object_or_404(Product, id=product_id)
    # form = CartAddProductForm(request.POST)
    # if form.is_valid():
    cart.add(product=product)

    return
