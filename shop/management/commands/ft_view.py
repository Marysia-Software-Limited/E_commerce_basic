import flet as ft

from django.shortcuts import get_object_or_404

from shop.models import Product, Category


def main(page: ft.Page):
    # defining page title and ThemeMode control
    page.title = "Shop app Django/Flet"

    page.theme_mode = ft.ThemeMode.SYSTEM

    # category_images = ft.Row(expand=1, wrap=True,
    #                          alignment=ft.MainAxisAlignment.SPACE_EVENLY,
    #                          vertical_alignment=ft.CrossAxisAlignment.CENTER,
    #                          scroll="always")

    # define groups of items to be displayed in views, to be used as parameters to view functions:
    categories = Category.objects.all()

    products = Product.objects.filter(available=True)

    # define a logo for the app and its location
    logo = ft.Image(
        src=f"http://127.0.0.1:8000/media/img/logo.png",
        width=400,
        height=400,
        fit=ft.ImageFit.FILL,
    )

    # routing for a NavigationBar control in navbar function
    def products_url(_):
        return page.go('/products')

    def main_url(_):
        return page.go("/")

    def product_detail_url(id):
        def __wrap(e):
            return page.go(f'/product_detail&{id}')

        return __wrap

    def navbar(e):
        """
        Define the NavigationBar control behaviour.

        :param e: event
        :return: return routing url depending on
            a chosen button of NavigationBar control
        """
        if e.data == '0':
            return page.go('/')
        elif e.data == '1':
            return page.go('/products')
        # elif e.data == '2':
        #     return page.go('/map')

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(
                icon=ft.icons.HOME_OUTLINED,
                label="Home"),
            ft.NavigationDestination(
                icon=ft.icons.STORE_OUTLINED,
                label="Products"),
            # ft.NavigationDestination(
            #     icon=ft.icons.MAP_OUTLINED,
            #     label="Find us!"
            # )
        ],
        on_change=navbar
    )

    def route_change(route):
        """
        Define the views to be displayed on the app depending
        on the route defined by routing functions,
        clear page views and render new views.

        :param route: Route returned by routing functions
        :return: return page update to a required set of views.
        """
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("Endorsed by The Sea Nation"),
                              bgcolor=ft.colors.SURFACE_VARIANT,
                              center_title=True),
                    ft.Text('The Way It Should Be', style=ft.TextThemeStyle.DISPLAY_LARGE),
                    logo,
                    ft.Text('We founded Endorsed by The Sea Nation with one goal in mind: providing a high-quality, '
                            'smart, and reliable online store. Our passion for excellence has driven us from the '
                            'beginning and continues to drive us into the future. We know that every product counts, '
                            'and strive to make the entire shopping experience as rewarding as possible. Check it out '
                            'for yourself!',
                            text_align=ft.TextAlign.JUSTIFY,
                            style=ft.TextThemeStyle.TITLE_LARGE,
                            no_wrap=False,
                            ),
                    ft.ElevatedButton("List products",
                                      on_click=products_url),
                    page.navigation_bar,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )

        if page.route == "/products":
            page.views.clear()
            page.views.append(
                ft.View(
                    "/products",
                    [
                        ft.AppBar(title=ft.Text("Our products:"),
                                  bgcolor=ft.colors.SURFACE_VARIANT,
                                  center_title=True),
                        view_multiple(products),
                        page.navigation_bar,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )
        elif page.route.startswith('/product_detail'):
            id = page.route.rsplit('&')[1]
            page.views.clear()
            page.views.append(
                ft.View(
                    f"/product_detail&{id}",
                    [
                        ft.AppBar(title=ft.Text("Product details"),
                                  bgcolor=ft.colors.SURFACE_VARIANT,
                                  center_title=True),
                        view_product_detail(id),
                        page.navigation_bar,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    def view_multiple(items):
        """
        Display multiple elements of a group passed as a parameter.
        Return a responsive view of its elements.

        :param items: parameter passed to the view is a name of
            a group to be displayed (products, services, categories etc.)
        :return: return the responsive view of elements
            of the group passed as a parameter.
        """
        localhost = 'http://127.0.0.1:8000'
        items_list = ft.Row(expand=1, wrap=True,
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            scroll="always")

        for item in items:

            link = item.get_absolute_url()
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
                                             size=20,
                                             weight=ft.FontWeight.W_300,
                                             width=300,
                                             no_wrap=False),
                                     ft.Text(item.price,
                                             size=26,
                                             weight=ft.FontWeight.W_900)],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                ),
                            ]
                        ),
                        margin=10,
                        padding=10,
                        alignment=ft.alignment.center,
                        width=500,
                        height=650,
                        border_radius=10,
                        ink=True,
                        on_click=product_detail_url(item.id),
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
                                             no_wrap=False),
                                     ft.Text(item.price,
                                             size=26,
                                             weight=ft.FontWeight.W_900)],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                )
                            ]
                        ),
                        margin=10,
                        padding=10,
                        alignment=ft.alignment.center,
                        width=500,
                        height=650,
                        border_radius=10,
                        ink=True,
                        on_click=main_url,
                    )
                )

        return items_list

    def view_product_detail(item):
        """
        Display chosen element passed as a parameter.
        Return a responsive view of this element details.

        :param item: parameter passed to the view is an id of
            an element to be displayed (product, service, map etc.)
        :return: return the responsive view of elements
            of the group passed as a parameter.
        """
        product = get_object_or_404(Product, id=item)

        product_detail = ft.Row(expand=1, wrap=True,
                                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                scroll="always")
        localhost = 'http://127.0.0.1:8000'

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

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(target=main)
