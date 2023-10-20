from django.contrib import admin
from django.http.request import HttpRequest

from commerce.models import *

admin.site.site_header = 'Tina Store'

# Register your models here.
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name','email','phone','subject','message']

    def has_add_permission(self, request):
        return False
    
    # def has_delete_permission(self, request):
    #     return False
    
@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['product_name','product_price','created']
    search_fields = ['product_name']
    prepopulated_fields = {'slug':('product_name',)}

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    readonly_fields =['total_amount',]
    list_display =[
        'name','email','phone','product_name','quantity','amount','total_amount','address','paid','updated'
    ]
    list_filter = ['paid','created','product_name',]
    
    def has_add_permission(self, request) :
        return False
    
    def has_delete_permission(self, request, obj=None) :
        return False