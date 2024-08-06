from django.contrib import admin

from .models import *

class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [CarImageInline]

admin.site.register(Customer)
admin.site.register(Company)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
