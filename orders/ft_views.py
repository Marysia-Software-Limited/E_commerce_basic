import flet as ft

from flet_django.views import ft_view

from orders.models import Order, OrderItem
from orders.views import OrderCreateForm
from shop.models import Product
from shop.ft_views import product_detail_url, Localhost
from cart.ft_cart import CartFt


def order_form_view(page):

    def button_clicked(e):

        fields = [tb1.value, tb2.value, tb3.value, tb4.value, tb5.value, tb6.value]
        print(f'{fields}')
        return order_create(page, fields)

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
    tb6 = ft.TextField(label="City",
                       capitalization=ft.TextCapitalization.WORDS,
                       keyboard_type=ft.KeyboardType.STREET_ADDRESS)
    b = ft.ElevatedButton(text="Submit", on_click=button_clicked)

    return ft_view(
        page,
        controls=[
            tb1,
            tb2,
            tb3,
            tb4,
            tb5,
            tb6,
            b,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


def order_create(page, fields):

    cart = CartFt(page)
    total = 0
    form_names = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']
    form_fields = dict(map(lambda k, v: (k, v), form_names, fields))

    form = OrderCreateForm(form_fields)
    if form.is_valid():
        order = form.save()
        for item in iter(cart):
            OrderItem.objects.create(order=order,
                                     product=item['product'],
                                     price=item['price'],
                                     quantity=item['quantity'])
            total += int(item['price']) * int(item['quantity'])

        # clear the cart
        cart.clear()

        # # launching asynchronous task - send an email notification
        # order_created.delay(order.id, total)
        # # set up the order in the session
        # request.session['order_id'] = order.id
        # # redirect for payment
        # return redirect(reverse('payment:process'))
    else:
        return page.go(f'/order')

    return page.go(f'/thanks')

