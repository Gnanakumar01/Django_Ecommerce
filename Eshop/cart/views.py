from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Sum

from .models import CartItem
from products.models import Product


class AddToCart(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({
                'error': 'login_required',
                'redirect_url': reverse('signin')
            }, status=401)

        product_id = request.POST.get('product_id')
        this_product = get_object_or_404(Product, id=product_id)

        item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=this_product,
            defaults={"quantity": 1}
        )

        if not created:
            item.quantity += 1
            item.save()

        cart_count = CartItem.objects.filter(user=request.user).aggregate(
            total=Sum("quantity")
        )["total"] or 0

        return JsonResponse({
            'message': f'{this_product.title.capitalize()} was added to cart',
            'cart_count': cart_count
        })


@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, 'cart/cart.html', {'cart_items': cart_items})


@login_required
def get_cart_item_count(request):
    cart_count = CartItem.objects.filter(user=request.user).aggregate(
        total=Sum("quantity")
    )["total"] or 0

    return JsonResponse({'cart_count': cart_count})


# Quantity increase, decrease, remove

def get_cart_total(user):
    return (
        CartItem.objects.filter(user=user)
        .aggregate(total=Sum("subtotal"))["total"] or 0
    )


@login_required
def increase_quantity(request, product_id):
    item = get_object_or_404(CartItem, user=request.user, product_id=product_id)
    item.quantity += 1
    item.save()

    return JsonResponse({
        "quantity": item.quantity,
        "subtotal": item.subtotal,
        "cart_total": get_cart_total(request.user)
    })


@login_required
def decrease_quantity(request, product_id):
    item = get_object_or_404(CartItem, user=request.user, product_id=product_id)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
        quantity = item.quantity
    else:
        item.delete()
        quantity = 0

    return JsonResponse({
        "quantity": quantity,
        "subtotal": item.subtotal if quantity else 0,
        "cart_total": get_cart_total(request.user)
    })


@login_required
def remove_item(request, product_id):
    item = get_object_or_404(CartItem, user=request.user, product_id=product_id)
    item.delete()

    return JsonResponse({
        "cart_total": get_cart_total(request.user)
    })

