from django.urls import path,re_path
from .views import (
    products,
    productDetail,
    search_by_catagory,
    search_by_label,
    search_by_badge,
    item_list_view_by_tags,
    search,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
    ordersummary,
    delete_item,
)
from django.conf.urls.static import static
from django.conf import settings
app_name='ecommercewebapp'
urlpatterns = [
    path('',products.as_view(),name='home'),
    path('product/<slug>/',productDetail, name='product'),
    path('search/',search, name='search'),
    path('catagory/<str:catagory>',search_by_catagory,name='catagory'),
    path('label/<str:label>',search_by_label,name='label'),
    path('badge/<str:badge>',search_by_badge,name='badge'),
    path('tag/?P<tag_slug>[-\w]+/',item_list_view_by_tags,name='items_by_tag'),
    path('addtocart/<slug>',add_to_cart,name='add_to_cart'),
    path('removefromcart/<slug>',remove_from_cart,name='remove_from_cart'),
    path('removesingleitemfromcart/<slug>',remove_single_item_from_cart,name='remove_single_item_from_cart'),
    path('order-summary',ordersummary.as_view(),name='order_summary'),
    path('delete-item/<slug>',delete_item,name='delete_item'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)