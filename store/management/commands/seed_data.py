from django.core.management.base import BaseCommand
from store.models import Category, Product


CATEGORIES = ['Fruits', 'Vegetables', 'Dairy & Eggs', 'Bakery', 'Beverages', 'Snacks']

WIKI = 'https://commons.wikimedia.org/wiki/Special:FilePath/'

PRODUCTS = [
    ('Fruits', 'Fresh Bananas', 'Sweet ripe bananas, sold by the bunch.', 1.99, 'kg', 4.5, True, WIKI + 'Banana%20%28white%20background%29.jpg'),
    ('Fruits', 'Red Apples', 'Crisp and juicy red apples.', 2.49, 'kg', 4.6, True, WIKI + 'Red%20Apple.jpg'),
    ('Fruits', 'Strawberries', 'Sweet farm-fresh strawberries.', 3.99, 'pack', 4.8, False, WIKI + 'Strawberry%20on%20white%20background.jpg'),
    ('Vegetables', 'Roma Tomatoes', 'Fresh red tomatoes, perfect for salads.', 1.49, 'kg', 4.3, True, WIKI + 'Tomato%20je.jpg'),
    ('Vegetables', 'Baby Spinach', 'Washed and ready-to-eat baby spinach.', 2.29, 'pack', 4.4, False, WIKI + 'Spinach%20leaves.jpg'),
    ('Vegetables', 'Carrots', 'Crunchy fresh carrots.', 1.29, 'kg', 4.2, False, WIKI + 'Carrots.JPG'),
    ('Dairy & Eggs', 'Whole Milk', 'Farm fresh whole milk, 1 liter.', 1.79, 'each', 4.5, True, WIKI + 'Glass%20of%20milk.jpg'),
    ('Dairy & Eggs', 'Free-Range Eggs', 'Dozen free-range eggs.', 3.49, 'dozen', 4.7, True, WIKI + 'Egg%20on%20white%20background.jpg'),
    ('Dairy & Eggs', 'Cheddar Cheese', 'Aged cheddar cheese block.', 4.99, 'each', 4.6, False, WIKI + 'Cheese.jpg'),
    ('Bakery', 'Sourdough Bread', 'Freshly baked sourdough loaf.', 3.29, 'each', 4.6, True, WIKI + 'Sourdough%20Bread%20Loaf.jpg'),
    ('Bakery', 'Croissants', 'Buttery, flaky croissants, pack of 4.', 4.49, 'pack', 4.5, False, WIKI + 'Croissant-Petr%20Kratochvil.jpg'),
    ('Beverages', 'Orange Juice', 'Freshly squeezed orange juice, 1 liter.', 2.99, 'each', 4.4, False, WIKI + 'Orange%20juice%201%20edit1.jpg'),
    ('Beverages', 'Sparkling Water', 'Pack of 6 sparkling water cans.', 3.99, 'pack', 4.1, False, WIKI + 'Sparkling%20Water%20%284675945072%29.jpg'),
    ('Snacks', 'Mixed Nuts', 'Roasted mixed nuts, 250g.', 5.49, 'pack', 4.7, True, WIKI + 'Mixed%20nuts%20small%20white2.jpg'),
    ('Snacks', 'Potato Chips', 'Crispy salted potato chips.', 1.99, 'pack', 4.0, False, WIKI + 'Potato-Chips.jpg'),
]


class Command(BaseCommand):
    help = 'Seed the database with demo grocery categories and products'

    def handle(self, *args, **options):
        category_map = {}
        for name in CATEGORIES:
            slug = name.lower().replace(' & ', '-').replace(' ', '-')
            category, _ = Category.objects.get_or_create(name=name, defaults={'slug': slug})
            category_map[name] = category

        created_count = 0
        for cat_name, name, desc, price, unit, rating, featured, photo_url in PRODUCTS:
            product, created = Product.objects.get_or_create(
                name=name,
                defaults={
                    'category': category_map[cat_name],
                    'description': desc,
                    'price': price,
                    'unit': unit,
                    'rating': rating,
                    'is_featured': featured,
                    'stock': 50,
                    'image_url': photo_url,
                },
            )
            if created:
                created_count += 1
            elif not product.image and not product.image_url:
                product.image_url = photo_url
                product.save()

        self.stdout.write(self.style.SUCCESS(
            f'Seeded {len(CATEGORIES)} categories and {created_count} new products.'
        ))
