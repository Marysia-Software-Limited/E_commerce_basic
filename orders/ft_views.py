import flet as ft

from flet_django.views import ft_view

from orders.models import Order, OrderItem
from shop.models import Product
from shop.ft_views import product_detail_url, Localhost
from cart.ft_cart import CartFt


def order_form_view(page):
    cart = CartFt(page)
    total = 0

    tb1 = ft.TextField(label="Name",
                       capitalization=ft.TextCapitalization.WORDS,
                       keyboard_type=ft.KeyboardType.NAME)
    tb2 = ft.TextField(label="Surname",
                       capitalization=ft.TextCapitalization.WORDS,
                       keyboard_type=ft.KeyboardType.NAME)
    tb3 = ft.TextField(label="Email",
                       capitalization=ft.TextCapitalization.NONE,
                       keyboard_type=ft.KeyboardType.EMAIL)
    tb4 = ft.TextField(label="Address",
                       capitalization=ft.TextCapitalization.WORDS,
                       keyboard_type=ft.KeyboardType.STREET_ADDRESS)
    tb5 = ft.TextField(label="Postcode",
                       capitalization=ft.TextCapitalization.CHARACTERS,
                       keyboard_type=ft.KeyboardType.STREET_ADDRESS)
    b = ft.ElevatedButton(text="Submit", on_click=lambda e: page.go(f'/cart'))

    return ft_view(
                page,
                controls=[
                    tb1,
                    tb2,
                    tb3,
                    tb4,
                    tb5,
                    b,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )

#
# cart = Cart(request)
# total = 0
# if request.method == 'POST':
#     form = OrderCreateForm(request.POST)
#     if form.is_valid():
#         order = form.save()
#         for item in cart:
#             OrderItem.objects.create(order=order,
#                                      product=item['product'],
#                                      price=item['price'],
#                                      quantity=item['quantity'])
#             total += int(item['price']) * int(item['quantity'])
#         # clear the cart
#         cart.clear()
#
#         # launching asynchronous task - send an email notification
#         order_created.delay(order.id, total)
#         # set up the order in the session
#         request.session['order_id'] = order.id
#         # redirect for payment
#         return redirect(reverse('payment:process'))
#
# else:
#     form = OrderCreateForm()
#
# return render(request,
#               'orders/order/create.html',
#               {'cart': cart, 'form': form})
