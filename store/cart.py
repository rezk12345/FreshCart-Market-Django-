from decimal import Decimal
from .models import Product

CART_SESSION_KEY = 'cart'


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_KEY)
        if not cart:
            cart = self.session[CART_SESSION_KEY] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        pid = str(product.id)
        current_qty = self.cart.get(pid, {}).get('quantity', 0)
        new_qty = min(current_qty + quantity, product.stock)
        new_qty = max(new_qty, 0)
        if new_qty <= 0:
            return 0
        self.cart[pid] = {'quantity': new_qty, 'price': str(product.price)}
        self.save()
        return new_qty

    def set_quantity(self, product, quantity):
        pid = str(product.id)
        quantity = min(quantity, product.stock)
        if pid in self.cart:
            if quantity <= 0:
                del self.cart[pid]
            else:
                self.cart[pid]['quantity'] = quantity
            self.save()
        return max(quantity, 0)

    def remove(self, product):
        pid = str(product.id)
        if pid in self.cart:
            del self.cart[pid]
            self.save()

    def clear(self):
        self.session[CART_SESSION_KEY] = {}
        self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        products_map = {str(p.id): p for p in products}
        for pid, item in self.cart.items():
            product = products_map.get(pid)
            if not product:
                continue
            price = Decimal(item['price'])
            yield {
                'product': product,
                'quantity': item['quantity'],
                'price': price,
                'subtotal': price * item['quantity'],
            }

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
