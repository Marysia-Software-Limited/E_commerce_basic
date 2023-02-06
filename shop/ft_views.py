import flet as ft

from django.shortcuts import get_object_or_404
from flet_django.views import ft_view
from shop.models import Product, Category

categories = Category.objects.all()

products = Product.objects.filter(available=True)

localhost = 'http://127.0.0.1:8000'

# define a logo for the app and its location
logo = ft.Image(
    src=f"{localhost}/media/img/logo.png",
    width=200,
    height=200,
    fit=ft.ImageFit.FILL,
)


def product_detail_url(page, id):
    def __wrap(e):
        return page.go(f'/product_detail&{id}')

    return __wrap


def category_detail_url(page, id):
    def __wrap(e):
        return page.go(f'/category_detail&{id}')

    return __wrap


def list_items(page, items, kind):
    detail_link = ''

    items_list = ft.Row(expand=1, wrap=True,
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        scroll="always")

    for item in items:

        if kind == 'product':
            detail_link = product_detail_url(page, item.id)
        elif kind == 'category':
            detail_link = category_detail_url(page, item.id)

        if item.image:

            items_list.controls.append(
                ft.Container(
                    content=ft.Column(
                        [ft.Image(
                            src=f"{localhost}{item.image.url}",
                            width=500,
                            height=500,
                            fit=ft.ImageFit.FILL,
                            repeat=ft.ImageRepeat.NO_REPEAT,
                            border_radius=ft.border_radius.all(10),
                        ),
                            ft.Row(
                                [ft.Text(item.name,
                                         size=30,
                                         weight=ft.FontWeight.W_300,
                                         width=300,
                                         height=100,
                                         no_wrap=False)],
                                alignment=ft.MainAxisAlignment.CENTER
                            ),
                        ]
                    ),
                    margin=10,
                    padding=10,
                    alignment=ft.alignment.center,
                    width=500,
                    height=600,
                    border_radius=10,
                    ink=True,
                    on_click=detail_link,

                )
            )

        else:
            items_list.controls.append(
                ft.Container(
                    content=ft.Column(
                        [ft.Card(
                            ft.Column(
                                [
                                    ft.Row(height=250),
                                    ft.Text('No photo available now',
                                            width=500,
                                            height=250,
                                            size=26,
                                            weight=ft.FontWeight.W_600,
                                            text_align=ft.TextAlign.CENTER
                                            ),
                                ]
                            )
                        ),
                            ft.Row(
                                [ft.Text(item.name,
                                         size=20,
                                         weight=ft.FontWeight.W_300,
                                         width=300,
                                         no_wrap=False)],
                                alignment=ft.MainAxisAlignment.CENTER
                            )
                        ]
                    ),
                    margin=10,
                    padding=10,
                    alignment=ft.alignment.center,
                    width=500,
                    height=600,
                    border_radius=10,
                    ink=True,
                    on_click=detail_link,
                )
            )
    return items_list


def detail_view(page, item, kind):

    if kind == 'category':

        category = get_object_or_404(Category, id=item)
        products_filtered = products.filter(category=category)
        return list_items(page, products_filtered, 'product')

    elif kind == 'product':

        product = get_object_or_404(Product, id=item)

        product_detail = ft.Row(expand=1, wrap=True,
                                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                scroll="always")

        product_detail.controls.append(
            ft.ResponsiveRow([
                ft.Container(
                    ft.Image(
                        src=f"{localhost}{product.image.url}",
                        width=500,
                        height=500,
                        fit=ft.ImageFit.FILL,
                        repeat=ft.ImageRepeat.NO_REPEAT,
                        border_radius=ft.border_radius.all(10),
                    ),
                    padding=1,
                    col={"lg": 4},
                ),
                ft.Container(
                    ft.Column([
                        ft.Text(f'{product.name}',
                                size=26,
                                weight=ft.FontWeight.W_300,
                                width=500,
                                height=250,
                                no_wrap=False),
                        ft.Text(f'{product.category}',
                                size=20,
                                weight=ft.FontWeight.W_300,
                                width=500,
                                height=100,
                                no_wrap=False),
                        ft.Text(f'£ {product.price}',
                                size=26,
                                weight=ft.FontWeight.W_900,
                                width=500,
                                height=50,
                                no_wrap=False),
                    ],
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    ),
                    padding=1,
                    col={"lg": 2},
                ),
                ft.Container(
                    ft.Column([
                        ft.Text(f'{product.description}',
                                size=20,
                                weight=ft.FontWeight.W_300,
                                # width=500,
                                # height=100,
                                no_wrap=False),
                    ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    padding=1,
                    col={"lg": 6},
                ),
            ]
            )
        )

        return product_detail


def home(page):
    return ft_view(
        page,
        controls=[ft.Text('The Way It Should Be', style=ft.TextThemeStyle.DISPLAY_LARGE),
                  logo,
                  ft.Text(
                      'We founded Endorsed by The Sea Nation with one goal in mind: providing a high-quality,'
                      'smart, and reliable online store. Our passion for excellence has driven us from the '
                      'beginning and continues to drive us into the future. We know that every product '
                      'counts,'
                      'and strive to make the entire shopping experience as rewarding as possible. Check it '
                      'out'
                      'for yourself!',
                      text_align=ft.TextAlign.JUSTIFY,
                      style=ft.TextThemeStyle.TITLE_LARGE,
                      no_wrap=False,
                  ),
                  list_items(page, categories, 'category'),
                  ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.colors.BLACK26,
    )


def products_view(page):
    return ft_view(
        page,
        controls=[
            list_items(page, products, 'product'),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


def categories_view(page):
    return ft_view(
        page,
        controls=[
            list_items(page, categories, 'category'),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


def category_detail_view(page, id):
    return ft_view(
        page,
        controls=[
            detail_view(page, id, 'category')
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


def product_detail_view(page, id):
    return ft_view(
        page,
        controls=[
            detail_view(page, id, 'product')
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
