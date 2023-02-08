import flet as ft

from flet_django.views import ft_view

from shop.models import Product
from shop.ft_views import product_detail_url, Localhost
from .ft_cart import CartFt


def cart_detail(page):
    cart = CartFt(page)

    # items_list = ft.Column(alignment=ft.MainAxisAlignment.SPACE_EVENLY,
    #                        scroll="always")

    items_list = ft.Column(alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                           scroll="always")

    items_list.controls.append(
        ft.Container(
            content=ft.Row(
                [ft.Text(
                    'Image',
                    size=20,
                    width=150,
                    weight=ft.FontWeight.W_300,
                ),
                    ft.Text('Product Name',
                            size=20,
                            width=150,
                            weight=ft.FontWeight.W_300,
                            no_wrap=False
                            ),
                    ft.Text('Quantity',
                            size=20,
                            width=90,
                            weight=ft.FontWeight.W_300,
                            no_wrap=False),
                    ft.Text('Price',
                            size=20,
                            width=75,
                            weight=ft.FontWeight.W_300,
                            no_wrap=False),
                    ft.Text('Total price',
                            size=20,
                            width=75,
                            weight=ft.FontWeight.W_600,
                            no_wrap=False),
                ],
                auto_scroll=True,
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            margin=10,
            padding=10,
            # width=800,
            alignment=ft.alignment.center,
            border_radius=10,
            ink=True,
            # on_click=detail_link,
        ))

    for item in iter(cart):
        # product = item.product
        # detail_link = product_detail_url(page, item.id)
        product = Product.objects.get(name=item['product'])

        if product.image:

            items_list.controls.append(
                ft.Container(
                    content=ft.Row(
                        [ft.Image(
                            src=f"{Localhost}{product.image.url}",
                            width=150,
                            height=150,
                            fit=ft.ImageFit.FILL,
                            repeat=ft.ImageRepeat.NO_REPEAT,
                            border_radius=ft.border_radius.all(10),
                        ),
                            ft.Text(item['product'],
                                    size=20,
                                    width=150,
                                    weight=ft.FontWeight.W_300,
                                    no_wrap=False
                                    ),
                            ft.Text(item['quantity'],
                                    size=20,
                                    width=80,
                                    weight=ft.FontWeight.W_300,
                                    no_wrap=False),
                            ft.Text(item['price'],
                                    size=20,
                                    width=75,
                                    weight=ft.FontWeight.W_300,
                                    no_wrap=False),
                            ft.Text(item['total_price'],
                                    size=20,
                                    width=75,
                                    weight=ft.FontWeight.W_600,
                                    no_wrap=False),
                        ],
                        auto_scroll=True,
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    margin=10,
                    padding=10,
                    # width=800,
                    alignment=ft.alignment.center,
                    border_radius=10,
                    ink=True,
                    # on_click=detail_link,
                )
            )

        else:
            items_list.controls.append(
                ft.Container(
                    content=ft.ListView(
                        [ft.Text('No photo available now',
                                 width=200,
                                 height=100,
                                 size=12,
                                 weight=ft.FontWeight.W_600,
                                 text_align=ft.TextAlign.CENTER
                                 ),
                         ft.Text(item.name,
                                 size=20,
                                 weight=ft.FontWeight.W_300,
                                 no_wrap=False),
                         ft.Text(item['quantity'],
                                 size=20,
                                 weight=ft.FontWeight.W_300,
                                 no_wrap=False),
                         ft.Text(item['price'],
                                 size=20,
                                 weight=ft.FontWeight.W_300,
                                 no_wrap=False),
                         ft.Text(item['total_price'],
                                 size=20,
                                 weight=ft.FontWeight.W_600,
                                 no_wrap=False),
                         ft.Text(CartFt.get_total_price(),
                                 size=20,
                                 weight=ft.FontWeight.W_600,
                                 no_wrap=False),
                         ],
                        auto_scroll=True,
                        first_item_prototype=True,
                        horizontal=True,

                    ),
                    margin=10,
                    padding=10,
                    alignment=ft.alignment.center,
                    border_radius=10,
                    ink=True,
                    # on_click=detail_link,
                )
            )

    items_list.controls.append(
        ft.Container(
            content=ft.Row(
                [ft.Text(
                    '',
                    size=20,
                    width=200,
                    weight=ft.FontWeight.W_300,
                ),
                    ft.Text('',
                            size=20,
                            width=100,
                            weight=ft.FontWeight.W_300,
                            no_wrap=False
                            ),
                    ft.Text('',
                            size=20,
                            width=50,
                            weight=ft.FontWeight.W_300,
                            no_wrap=False),
                    ft.Text(
                        'Total amount:',
                        size=30,
                        weight=ft.FontWeight.W_600,
                        no_wrap=False,
                    ),
                    ft.Text(cart.get_total_price(),
                            size=30,
                            width=120,
                            weight=ft.FontWeight.W_600,
                            no_wrap=False),
                ],
                auto_scroll=True,
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            margin=10,
            padding=10,
            # width=800,
            alignment=ft.alignment.center,
            border_radius=10,
            ink=True,
            # on_click=detail_link,
        ))

    return items_list


def cart_view(page):
    return ft_view(
        page,
        controls=[
            cart_detail(page),
            ft.FilledButton('Order', on_click=lambda e:page.go(f'/order'))
            # cart_total(page),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
