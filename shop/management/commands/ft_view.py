import flet as ft

# from os.path import join
from shop.models import Product, Category
# from E_commerce_basic.settings import BASE_DIR as base_dir


def main(page: ft.Page):
    page.title = "Product List"

    page.theme_mode = ft.ThemeMode.SYSTEM

    def store_url(_):
        return page.go('/store')

    def main_url(_):
        return page.go("/")

    def navbar(e):
        if e.data == '0':
            return page.go('/')
        elif e.data == '1':
            return page.go('/store')

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(
                icon=ft.icons.HOME_OUTLINED,
                label="Home"),
            ft.NavigationDestination(
                icon=ft.icons.STORE_OUTLINED,
                label="Store"),
        ],
        on_change=navbar
    )

    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("Flet app"), bgcolor=ft.colors.SURFACE_VARIANT, center_title=True),
                    ft.ElevatedButton("Visit Store", on_click=store_url),
                    page.navigation_bar,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )

        if page.route == "/store":
            page.views.clear()
            page.views.append(
                ft.View(
                    "/store",
                    [
                        logo,
                        images,
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
    images = ft.Row(expand=1, wrap=True, scroll="always")

    # for i in range(0, 30):
    #     images.controls.append(
    #         ft.ElevatedButton(
    #             style=ft.ButtonStyle(
    #
    #                 overlay_color=ft.colors.TRANSPARENT,
    #                 elevation={"pressed": 0, "": 0},
    #             ),
    #             content=ft.Image(
    #                 src=f"https://picsum.photos/300/?{i}",
    #                 # width=200,
    #                 # height=200,
    #                 fit=ft.ImageFit.FILL,
    #                 repeat=ft.ImageRepeat.NO_REPEAT,
    #                 border_radius=ft.border_radius.all(10),
    #             ),
    #             on_click=main_url,
    #         )
    #     )

    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    for product in products:

        link = product.get_absolute_url()
        localhost = 'http://127.0.0.1:8000'

        if product.image:
            # image_link = join(base_dir, product.image.url)
            images.controls.append(
                ft.ElevatedButton(
                    style=ft.ButtonStyle(

                        overlay_color=ft.colors.TRANSPARENT,
                        elevation={"pressed": 0, "": 0},
                    ),
                    content=ft.Image(
                        src=f"{localhost}{product.image.url}",
                        width=200,
                        height=200,
                        fit=ft.ImageFit.FILL,
                        repeat=ft.ImageRepeat.NO_REPEAT,
                        border_radius=ft.border_radius.all(10),
                    ),
                    on_click=link,
                )
            )
            print(f'{localhost}{product.image.url}')
        else:
            images.controls.append(
                ft.ElevatedButton(
                    style=ft.ButtonStyle(

                        overlay_color=ft.colors.TRANSPARENT,
                        elevation={"pressed": 0, "": 0},
                    ),
                    content=ft.Image(
                        src=f"static/img/no_image.png",
                        width=200,
                        height=200,
                        fit=ft.ImageFit.FILL,
                        repeat=ft.ImageRepeat.NO_REPEAT,
                        border_radius=ft.border_radius.all(10),
                    ),
                    on_click=link,
                )
            )
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(target=main)
