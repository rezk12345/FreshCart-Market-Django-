from django.contrib import admin
from .models import Category, Product, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'rating', 'is_featured')
    list_filter = ('category', 'is_featured')
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock', 'is_featured')
    fields = ('category', 'name', 'description', 'price', 'unit', 'rating', 'stock', 'is_featured', 'image', 'image_url')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'phone', 'total_price', 'created_at', 'items_summary')
    search_fields = ('customer_name', 'phone')
    inlines = [OrderItemInline]

    def items_summary(self, obj):
        return ', '.join(f'{item.quantity} x {item.product.name}' for item in obj.items.all())
    items_summary.short_description = 'Items ordered'
