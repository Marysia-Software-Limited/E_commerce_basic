import flet as ft
from shop.ft_urls import urlpatterns
from shop.models import Product, Category
from flet_django.pages import GenericApp
from flet_django.navigation import Fatum


destinations = [
    Fatum(
        route="/",
        icon=ft.icons.HOME_OUTLINED,
        selected_icon=ft.icons.HOME_OUTLINED,
        label="Home",
        nav_bar=True,
        action=True,
        nav_rail=False
    ),
    Fatum(
        route="/products",
        icon=ft.icons.STORE_OUTLINED,
        selected_icon=ft.icons.STORE_OUTLINED,
        label="Products",
        nav_bar=True,
        action=True,
        nav_rail=False
    ),
    Fatum(
        route="/categories",
        icon=ft.icons.MAP_OUTLINED,
        selected_icon=ft.icons.MAP_OUTLINED,
        label="Categories",
        nav_bar=True,
        action=True,
        nav_rail=False
    ),
    Fatum(
        route="/cart",
        icon=ft.icons.SHOPPING_CART,
        selected_icon=ft.icons.SHOPPING_CART,
        label="Cart",
        nav_bar=True,
        action=True,
        nav_rail=False
    ),
]

main = GenericApp(
    destinations=destinations,
    urls=urlpatterns,
    init_route="/",
    view_params={
        'app_bar_params': dict(
            title="Endorsed by The Sea Nation",
            bgcolor=ft.colors.BLACK38,
            center_title=True),
    },
)
