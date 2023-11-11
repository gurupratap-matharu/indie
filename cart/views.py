import logging

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from properties.models import Room

from .cart import Cart
from .forms import CartAddProductForm

logger = logging.getLogger(__name__)


@require_POST
@csrf_exempt
def cart_add(request, product_id):
    """
    Add a product to the cart. Does not render a template
    """

    cart = Cart(request)
    product = get_object_or_404(Room, id=product_id)
    form = CartAddProductForm(request.POST)
    # quantity = int(request.session["q"]["num_of_passengers"])

    if form.is_valid():
        logger.info("cart form is valid...")
        cd = form.cleaned_data
        cart.add(
            product=product, quantity=cd["quantity"], override_quantity=cd["override"]
        )

    logger.warning("⚠️ cart form in invalid...")

    return redirect("cart:cart-detail")


@require_POST
def cart_remove(request, product_id):
    """
    Remove a product to the cart. Does not render a template
    """

    product = get_object_or_404(Room, id=product_id)

    cart = Cart(request)
    cart.remove(product)

    messages.success(request, "Item successfully removed from the cart. ✅")

    return redirect("cart:cart-detail")


def cart_detail(request):
    """
    Detail view to show all the contents in a cart.
    """

    cart = Cart(request)
    template_name = "cart/cart_detail.html"
    context = {"cart": cart}

    return render(request, template_name, context)
