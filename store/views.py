import json
from decimal import Decimal

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .cart import Cart
from .forms import CheckoutForm
from .models import Category, Product, Order, OrderItem


def home(request):
    categories = Category.objects.all()
    featured_products = Product.objects.filter(is_featured=True)[:8]
    if not featured_products:
        featured_products = Product.objects.all()[:8]
    context = {
        'categories': categories,
        'featured_products': featured_products,
    }
    return render(request, 'store/home.html', context)


def product_list(request):
    products = Product.objects.select_related('category').all()
    categories = Category.objects.all()

    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()

    if query:
        products = products.filter(name__icontains=query)

    if category_slug:
        products = products.filter(category__slug=category_slug)

    context = {
        'products': products,
        'categories': categories,
        'query': query,
        'active_category': category_slug,
    }
    return render(request, 'store/product_list.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(category=product.category).exclude(pk=pk)[:4]
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'store/product_detail.html', context)


def cart_detail(request):
    cart = Cart(request)
    context = {'cart': cart}
    return render(request, 'store/cart.html', context)


@require_POST
def cart_add(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = Cart(request)
    requested_qty = int(request.POST.get('quantity', 1))
    current_qty_in_cart = cart.cart.get(str(product.pk), {}).get('quantity', 0)
    final_qty = cart.add(product, quantity=requested_qty)
    capped = final_qty < current_qty_in_cart + requested_qty
    return JsonResponse({
        'success': True,
        'cart_count': len(cart),
        'cart_total': str(cart.total_price()),
        'quantity_in_cart': final_qty,
        'capped': capped,
        'stock': product.stock,
    })


@require_POST
def cart_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = Cart(request)
    requested_qty = int(request.POST.get('quantity', 1))
    final_qty = cart.set_quantity(product, requested_qty)
    capped = final_qty < requested_qty
    return JsonResponse({
        'success': True,
        'cart_count': len(cart),
        'cart_total': str(cart.total_price()),
        'quantity_in_cart': final_qty,
        'capped': capped,
        'stock': product.stock,
    })


@require_POST
def cart_remove(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = Cart(request)
    cart.remove(product)
    return JsonResponse({
        'success': True,
        'cart_count': len(cart),
        'cart_total': str(cart.total_price()),
    })


def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.info(request, 'Your cart is empty. Add some groceries first.')
        return redirect('store:product_list')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.total_price = cart.total_price()
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['price'],
                )
            cart.clear()
            return redirect('store:order_success', pk=order.pk)
    else:
        form = CheckoutForm()

    context = {'cart': cart, 'form': form}
    return render(request, 'store/checkout.html', context)


def order_success(request, pk):
    order = get_object_or_404(Order, pk=pk)
    context = {'order': order}
    return render(request, 'store/success.html', context)
