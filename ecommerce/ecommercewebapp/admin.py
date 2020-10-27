from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import MyUser,Profile,Item,OrderItem,Order
class ItemAdmin(admin.ModelAdmin):
    list_display = ['title','price','slug','img']
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['user','item','quantity','ordered']
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','start_date','order_date','Ordered']
admin.site.register(MyUser,UserAdmin)
admin.site.register(Profile)
admin.site.register(Item,ItemAdmin)
admin.site.register(OrderItem)
admin.site.register(Order,OrderAdmin)
