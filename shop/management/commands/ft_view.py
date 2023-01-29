import flet as ft

# from os.path import join
from shop.models import Product, Category


# from E_commerce_basic.settings import BASE_DIR as base_dir


def main(page: ft.Page):
    page.title = "Product List"

    page.theme_mode = ft.ThemeMode.SYSTEM

    def products_url(_):
        return page.go('/products')

    def main_url(_):
        return page.go("/")

    def navbar(e):
        if e.data == '0':
            return page.go('/')
        elif e.data == '1':
            return page.go('/products')

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(
                icon=ft.icons.HOME_OUTLINED,
                label="Home"),
            ft.NavigationDestination(
                icon=ft.icons.STORE_OUTLINED,
                label="Products"),
        ],
        on_change=navbar
    )

    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("Endorsed by The Sea Nation"),
                              bgcolor=ft.colors.SURFACE_VARIANT,
                              center_title=True),
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
                        product_images,
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

    logo = ft.Image(
        src=f"/icons/icon-512.png",
        width=100,
        height=100,
        fit=ft.ImageFit.FILL,
    )
    product_images = ft.Row(expand=1, wrap=True,
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            scroll="always")

    category_images = ft.Row(expand=1, wrap=True, scroll='always')

    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    for product in products:

        link = product.get_absolute_url()
        localhost = 'http://127.0.0.1:8000'

        if product.image:
            # image_link = join(base_dir, product.image.url)
            product_images.controls.append(
                ft.Container(
                    content=ft.Column(
                        [ft.Image(
                            src=f"{localhost}{product.image.url}",
                            width=500,
                            height=500,
                            fit=ft.ImageFit.FILL,
                            repeat=ft.ImageRepeat.NO_REPEAT,
                            border_radius=ft.border_radius.all(10),
                        ),
                            ft.Row(
                                [ft.Text(product.name,
                                         size=20,
                                         weight=ft.FontWeight.W_300),
                                 ft.Text(product.price,
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
                    height=550,
                    border_radius=10,
                    ink=True,
                    on_click=main_url,

                )
            )
            print(f'{localhost}{product.image.url}')
        else:
            product_images.controls.append(
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
                                [ft.Text(product.name,
                                         size=20,
                                         weight=ft.FontWeight.W_300),
                                 ft.Text(product.price,
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
                    height=550,
                    border_radius=10,
                    ink=True,
                    on_click=main_url,
                )
            )

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(target=main)
