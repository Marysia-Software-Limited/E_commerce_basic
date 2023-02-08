import flet as ft

from django.shortcuts import get_object_or_404
from flet_django.views import ft_view
from shop.models import Product, Category
from cart.ft_cart import CartFt

# definitions for commonly used variables


Localhost = 'http://127.0.0.1:8000'

# define a logo for the app and its location
logo = ft.Image(
    src=f"{Localhost}/media/img/logo.png",
    width=200,
    height=200,
    fit=ft.ImageFit.FILL,
)


# block with helper functions facilitating access to data or urls according to need
def get_categories():
    return Category.objects.all()


def get_products():
    return Product.objects.filter(available=True)


def product_detail_url(page, id):
    def __wrap(e):
        return page.go(f'/product_detail&{id}')

    return __wrap


def category_detail_url(page, id):
    def __wrap(e):
        return page.go(f'/category_detail&{id}')

    return __wrap


def products_url(page):
    def __wrap(e):
        return page.go(f'/products')

    return __wrap


def categories_url(page):
    def __wrap(e):
        return page.go(f'/categories')

    return __wrap


def cart_url(page):
    def __wrap(e):
        return page.go(f'/cart')

    return __wrap


def list_items(page, items, kind):
    """
    Display chosen group passed as a parameter.
    Return a responsive view of group elements.

    :param page: This is a session object; Page is a container for View controls.
        A page instance and the root view are automatically
        created when a new user session started.
        See detailed info at https://flet.dev/docs/controls/page
    :param kind: define what group of data is being used (products|categories|other)
        Parameter is used for defining the details of accessing data,
        information displayed and urls used.
    :param items: parameter passed to the view is
        a list of elements to be displayed
        (products, services, categories etc.)
    :return: return the responsive view of elements
        of the group passed as a parameter.
    """

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
                            src=f"{Localhost}{item.image.url}",
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


def item_detail(page, item, kind):
    """
    Display chosen element passed as a parameter.
    Return a responsive view of the element details
    depending on its type.

    :param page: This is a session object; Page is a container for View controls.
        A page instance and the root view are automatically
        created when a new user session started.
        See detailed info at https://flet.dev/docs/controls/page
    :param kind: define what group of data is being used (products|categories|other)
        Parameter is used for defining the details of accessing data,
        information displayed and urls used.
    :param item: parameter passed to the view is an id of
        an element to be displayed (product, service, map etc.)
    :return: return the responsive view of elements
        of the group passed as a parameter.
    """
    products = get_products()

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
                        src=f"{Localhost}{product.image.url}",
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
                        ft.FilledButton(text='Add to cart',
                                        icon=ft.icons.SHOPPING_CART,
                                        on_click=lambda e:cart_add(page, item)),
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


# block with functions defining particular views in the app
def home(page):
    categories = get_categories()
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
    products = get_products()
    return ft_view(
        page,
        controls=[
            list_items(page, products, 'product'),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


def categories_view(page):
    categories = get_categories()
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
            item_detail(page, id, 'category')
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


def product_detail_view(page, id):

    return ft_view(
        page,
        controls=[
            item_detail(page, id, 'product'),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


def cart_add(page, product_id):
    """
    Receive product ID as a parameter and
    retrieve the Product instance with given ID;
    Validate CartAddProductForm - if valid,
    add or update item in the cart and redirect
    to the cart_detail URL to display cart contents.
    :param page: This is a session object; Page is a container for View controls.
        A page instance and the root view are automatically
        created when a new user session started.
        See detailed info at https://flet.dev/docs/controls/page
    :param product_id: passing product id value
    :return: redirect to the cart_detail page.
    """
    cart = CartFt(page)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product)
    cart.save()

    # test printouts
    # print(cart.get_total_price())

    for item in iter(cart):
        print(item)

    return
