import logging
from decimal import Decimal

from django.conf import settings

from properties.models import Room

logger = logging.getLogger(__name__)


class Cart:
    def __init__(self, request):
        """
        Initialize a cart.
        """

        logger.info("initializing cart...")

        self.session = request.session
        self.cart = self.session.setdefault(settings.CART_SESSION_ID, {})

    def get_total_price(self):
        """
        Calculate the total price across of the cart.
        """

        return sum(
            Decimal(item["price"]) * item["quantity"] for item in self.cart.values()
        )

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """

        logger.info(
            "adding to cart product:{product} quantity:{quantity}",
            extra={"product": product, "quantity": quantity},
        )

        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0, "price": str(product.weekday_price)}

        if override_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity

        self.save()

    def remove(self, product):
        """
        Remove a product from the cart.
        """

        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        """
        Marks the session as `modified` to make sure it gets saved.
        """

        logger.info("saving the cart...")
        self.session.modified = True

    def clear(self):
        """
        Removes the cart from the session
        """

        logger.info("clearing the cart...")

        del self.session[settings.CART_SESSION_ID]
        self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database.
        """

        product_ids = self.cart.keys()

        products = Room.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]["product"] = product

        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        """
        Count all the items in the cart.
        """

        return sum(item["quantity"] for item in self.cart.values())
