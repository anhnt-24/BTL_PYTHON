from django.contrib import admin
from .models import *

class SliderAdmin(admin.ModelAdmin):
    list_display = ('id', 'img', 'created_at', 'updated_at')  

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'name', 'phone', 'img', 'gender' ,'birth', 'created_at', 'updated_at') 

class GeneralCategoryAdmin(admin.ModelAdmin):
    list_display = ( 'id','name','img', "nameImg", 'created_at', 'updated_at',)  

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id' ,'name', 'general_category', 'created_at', 'updated_at')

class ProductAdmin(admin.ModelAdmin):
    list_display = ( 'id','name', 'category', 'price', 'created_at', 'updated_at')

class ColorAdmin(admin.ModelAdmin):
    list_display = ('product', 'color','img', 'created_at', 'updated_at')


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'quantity', 'price', 'total')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','code','user', 'total','created_at')

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id','order', 'color_size', 'quantity', 'total', 'status', 'delivered_at')

class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ( 'id','user','receiver', 'phone', 'province', 'district', 'commune', 'detail', 'created_at', 'updated_at')

class DiscountAdmin(admin.ModelAdmin):
    list_display = ('id','code','discount','created_at')

admin.site.register(Customer,CustomerAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem,OrderItemAdmin)
admin.site.register(Discount,DiscountAdmin)
admin.site.register(Slider, SliderAdmin)
# admin.site.register(ShippingAddress, ShippingAddressAdmin)
# admin.site.register(Color,ColorAdmin)
# admin.site.register(Category,CategoryAdmin)
# admin.site.register(GeneralCategory,GeneralCategoryAdmin)
# admin.site.register(CartItem,CartItemAdmin)