from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Item, OrderItem,Order
from taggit.models import Tag
from django.views.generic import ListView,DetailView,View
from django.shortcuts import get_object_or_404,redirect
from django.db.models import Count
from django.contrib.postgres.search import SearchVector,SearchQuery,SearchRank
from django.contrib.postgres.aggregates import StringAgg
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
class products(ListView):
    model = Item
    template_name = 'ecommercewebapp/products.html'
def productDetail(request,slug):
    item=get_object_or_404(Item,slug=slug)
    item_tags_ids=item.tags.values_list('id',flat=True)
    similar_items=Item.objects.filter(tags__in=item_tags_ids).exclude(id=item.id)
    similar_items=similar_items.annotate(same_tag=Count('tags'))
    context={
        'item':item,
        'similar_items':similar_items,
    }
    return render(request,'ecommercewebapp/product.html',context)
def search_by_catagory(request,catagory):
    items=Item.objects.filter(catagory=catagory)
    context={
        'items':items,
        'catagory':catagory
    }
    return render(request,'ecommercewebapp/search_by_catagory.html',context)
def search_by_label(request,label):
    items=Item.objects.filter(label=label)
    context={
        'items':items,
        'label':label
    }
    return render(request,'ecommercewebapp/search_by_label.html',context)
def search_by_badge(request,badge):
    items=Item.objects.filter(badge=badge)
    context={
        'badge':badge,
        'items':items
    }
    return render(request,'ecommercewebapp/search_by_badge.html',context)
def item_list_view_by_tags(request,tag_slug):
    tag=get_object_or_404(Tag,slug=tag_slug)
    items=Item.objects.all()
    items=items.filter(tags__in=[tag])
    context={
        'tag':tag,
        'items':items
    }
    return render(request,'ecommercewebapp/items_list_by_tags.html',context)
def search(request):
    try:
        q=request.GET.get('q')
    except:
        q='Please enter the query'
    if q:
        query=SearchQuery(q)
        vector=SearchVector('catagory',weight='A')+SearchVector(StringAgg('tags__name',weight='B',delimiter=','))
        rate=SearchRank(vector,query)
        items=Item.objects.annotate(rank=rate).order_by('-rank')
        context={
            'items':items,
            'query':q
        }
        return render(request,'ecommercewebapp/search.html',context)
    else:
        items=Item.objects.all()
        context={
            'query':q,
            'items':items
        }
        return render(request,'ecommercewebapp/nosearch.html',context)

@login_required
def add_to_cart(request,slug):
    item=get_object_or_404(Item,slug=slug)
    order_item,created=OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs=Order.objects.filter(user=request.user,Ordered=False)
    print(order_qs)
    if order_qs.exists():
        order=order_qs[0]
        if order.items.filter(item__slug=slug).exists():
            order_item.quantity+=1
            order_item.save()
            return redirect('ecommercewebapp:order_summary')
        else:
            order.items.add(order_item)
            return redirect('ecommercewebapp:product',slug=slug)
    else:
        start_date=timezone.now()
        order_date=timezone.now()
        order=Order.objects.create(user=request.user,order_date=order_date,start_date=start_date)
        order.items.add(order_item)
        return redirect('ecommercewebapp:order_summary')
def remove_single_item_from_cart(request,slug):
    item=get_object_or_404(Item,slug=slug)
    order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
    order_qs=Order.objects.filter(user=request.user,Ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        if order.items.filter(item__slug=slug).exists():
            if order_item.quantity>1:
                order_item.quantity-=1
                order_item.save()
                return redirect("ecommercewebapp:order_summary")
            else:
                order_item.quantity=1
                return redirect("ecommercewebapp:order_summary")
def remove_from_cart(request,slug):
    item=get_object_or_404(Item,slug=slug)
    order_qs=Order.objects.filter(user=request.user,Ordered=False)
def delete_item(request,slug):
    item=get_object_or_404(Item,slug=slug)
    order_item=OrderItem.objects.get(item=item,user=request.user,ordered=False)
    order=Order.objects.filter(user=request.user,Ordered=False)[0]
    order.items.remove(order_item)
    order_item.delete()
    if not order.items.all():
        return redirect("ecommercewebapp:home")
    else:
        return redirect("ecommercewebapp:order_summary")


class ordersummary(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:
            order = Order.objects.get(user=self.request.user, Ordered=False)
            context={
                'object':order
            }
            return render(self.request, 'ecommercewebapp/order_summary.html', context)
        except ObjectDoesNotExist:
            redirect('/')





