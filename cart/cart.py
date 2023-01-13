from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart:

    def __init__(self, request):
        """
        Initialise the cart.
        Read the current session's cart.
        If there is no cart in the session creates an empty cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # saves an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add product to the cart or update the quantity
        :param product:
        :param quantity:
        :param override_quantity:
        :return:
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            # The price of the product is read on addition,
            # so subsequent changes to the product's price
            # won't affect products in the cart in the current session.
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
            if override_quantity:
                self.cart[product_id]['quantity'] = quantity
            else:
                self.cart[product_id]['quantity'] += quantity
            self.save()

    def save(self):
        """
        Mark the session as modified, so it gets saved.
        """
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart
        :param product:
        :return:
        """
        product_id = str(product.id)
        if product_id in self.cart:
            # if product is in the cart, it removes it
            # and saves modified cart.
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get products from the database.
        :return:
        """
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart.
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        :return: number of items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Count the total price of all items in the cart.
        :return: Total price for the whole cart.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """
        Remove cart from the session.
        """
        del self.cart.session[settings.CART_SESSION_ID]
        self.save()
