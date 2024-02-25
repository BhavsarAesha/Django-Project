from django.contrib import admin
from .models import(
    Customer,
    Product,
    Cart,
    OrderPlaced,
    Contact
)
# Register your models here.
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
 list_display = ['id', 'user', 'name', 'locality', 'city',
                 'zipcode', 'state']
 
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
 list_display = ['id', 'title', 'selling_price',
                 'discounted_price', 'description',
                 'brand', 'category', 'product_image']
 
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
 list_display = ['id', 'user', 'product', 'quantity','size']

@admin.register(OrderPlaced)
class OrderPlaceModelAdmin(admin.ModelAdmin):
 list_display = ['id', 'user', 'customer', 'product',
                 'quantity','size', 'ordered_date', 'status']
 
# @admin.register(Payment)
# class PaymentModelAdmin(admin.ModelAdmin):
#  list_display = ['id', 'user', 'amount', 'razorpay_order_id',
#                  'razorpay_payment_status','razorpay_payment_id', 'paid']
 
@admin.register(Contact)
class ContactModelAdmin(admin.ModelAdmin):
 list_display = ['id','name','email','subject','message']