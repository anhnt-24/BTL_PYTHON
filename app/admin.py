from django.contrib import admin
from .models import *

class SliderAdmin(admin.ModelAdmin):
    list_display = ('id', 'img', 'created_at', 'updated_at')  # Fields to display in the list view
    search_fields = ('id',)  # Add search functionality if needed

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'name', 'phone', 'img', 'gender' ,'birth', 'created_at', 'updated_at', 'role')  # Display all fields
    search_fields = ('user__username', 'email', 'first_name', 'last_name', 'phone')  # Allow searching by relevant fields
    list_filter = ('role',)  # Enable filtering by role

class GeneralCategoryAdmin(admin.ModelAdmin):
    list_display = ( 'id','name', 'description','img', 'created_at', 'updated_at',)  # Display all fields
    search_fields = ('id','name', 'description')  # Allow searching by name and description

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id' ,'name', 'general_category', 'description', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('general_category',)  # Allow filtering by general category

class ProductAdmin(admin.ModelAdmin):
    list_display = ( 'id','name', 'category', 'price', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('category',)

class ColorAdmin(admin.ModelAdmin):
    list_display = ('product', 'color','img', 'created_at', 'updated_at')
    search_fields = ('product__name', 'color')
    list_filter = ('product',)


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'quantity', 'price', 'total')
    search_fields = ('product__name',)  # Search by product name and color

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total','created_at')
    search_fields = ('user__username',)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'color_size', 'quantity', 'total', 'status', 'delivered_at')
    search_fields = ('product__name', )

class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ( 'id','user','receiver', 'phone', 'province', 'district', 'commune', 'detail', 'created_at', 'updated_at')
    search_fields = ('name', 'receiver', 'phone', 'province', 'district', 'commune', 'detail')
    list_filter = ('province', 'district', 'commune', 'created_at', 'updated_at')
    ordering = ('-created_at',)

admin.site.register(Customer,CustomerAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Color,ColorAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(GeneralCategory,GeneralCategoryAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem,OrderItemAdmin)
admin.site.register(CartItem,CartItemAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)
admin.site.register(Slider, SliderAdmin)