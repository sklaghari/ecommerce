from django import template
from ..models import Order,OrderItem

register=template.Library()
@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs=Order.objects.filter(user=user,Ordered=False)
        if qs.exists():
            order=qs[0]
            count=order.items.count()
            return count
    else:
        return 0
@register.filter
def cart_item_count2(user):
    count=0
    if user.is_authenticated:
        cart_qs=OrderItem.objects.filter(user=user,ordered=False)
        if cart_qs.exists():
            for cart_item in cart_qs:
                count+=cart_item.quantity
            return count
        else:
            return 0