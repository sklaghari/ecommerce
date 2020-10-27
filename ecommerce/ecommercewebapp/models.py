from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.shortcuts import reverse
from taggit.managers import TaggableManager

CATAGORY_CHOICES=(
    ('Breaker','Breaker'),
    ('VFD','VFD'),
    ('Steam Turbine','Steam Turbine'),
    ('Gas Turbine','Gas Turboine'),
    ('Transformer','Transformer'),
    ('Motor','Motor'),
    ('Other','Other')
)
LABEL_CHOICES=(
    ('Human Safety','Human Safety'),
    ('Energy Saving','Energy Saving'),
    ('Reliability Enhancement','Reliability Enhancement'),
)
BADGE_CATAGORY=(
    ('Best Seller','Best Seller'),
    ('Most Reliable','Most Reliable'),
    ('Top Performer','Top performer')
)
ADDRESS_CHOICES=(
    ('S','Shipping'),
    ('B','Billing')
)

class MyUser(AbstractUser):
    email=models.EmailField(unique=True)
    def __str__(self):
        return self.first_name
    pass
class Profile(models.Model):
    user=models.OneToOneField(MyUser,on_delete=models.CASCADE)
    avatar=models.ImageField(upload_to='avatar/%Y/%m/%d',null=True,blank=True)

    def __str__(self):
        return self.user.first_name+" "+self.user.last_name
class Item(models.Model):
    title=models.CharField(max_length=250)
    price=models.FloatField()
    discountPercentage=models.IntegerField(null=True,blank=True)
    catagory=models.CharField(choices=CATAGORY_CHOICES,max_length=30,null=True)
    label=models.CharField(choices=LABEL_CHOICES,max_length=50,null=True)
    badge=models.CharField(choices=BADGE_CATAGORY,max_length=50,null=True)
    slug=models.SlugField(max_length=255,unique=True, null=True, blank=True)
    img=models.ImageField()
    description=models.TextField(null=True)
    tags=TaggableManager()
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.title)
        super(Item, self).save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse('ecommercewebapp:product',kwargs={
            'slug':self.slug
        })
    def get_total_discounted_price(self):
        return self.price-(self.price*(self.discountPercentage/100))
    def get_absolute_url_catagory(self):
        return reverse('ecommercewebapp:catagory',kwargs={
            'catagory':self.catagory
        })
    def get_absolute_url_by_label(self):
        return reverse('ecommercewebapp:label',kwargs={
            'label':self.label
        })
    def get_absolute_url_by_badge(self):
        return reverse('ecommercewebapp:badge',kwargs={'badge':self.badge})
    def add_to_cart(self):
        return reverse('ecommercewebapp:add_to_cart',kwargs={'slug':self.slug})
    def remove_from_cart(self):
        return reverse('ecommercewebapp:remove_from_cart',kwargs={'slug':self.slug})
class OrderItem(models.Model):
    user=models.ForeignKey(MyUser,on_delete=models.CASCADE)
    item=models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    ordered=models.BooleanField(default=False)
    def __str__(self):
        return f"{self.quantity} of {self.item.title}"
    def total_item_price(self):
        return self.item.price*self.quantity
    def total_price(self):
        if self.item.discountPercentage:
            return self.quantity*self.item.get_total_discounted_price()
        else:
            return self.total_item_price()
    def amount_saved(self):
        return self.total_item_price()-(self.total_price())
class Order(models.Model):
    user=models.ForeignKey(MyUser,on_delete=models.CASCADE)
    items=models.ManyToManyField(OrderItem)
    start_date=models.DateField(auto_now_add=True)
    order_date=models.DateField()
    Ordered=models.BooleanField(default=False)
    being_delievered=models.BooleanField(default=False)
    received=models.BooleanField(default=False)
    refund_requested=models.BooleanField(default=False)
    refund_requested_date=models.DateField(max_length=255,blank=True,null=True)
    refund_granted=models.BooleanField(default=False)
    def total_order_price(self):
        total=0
        for cart_item in self.items.all():
            total+=cart_item.total_price()
        return total
    def total_amount_saved(self):
        total_saved=0
        for cart_item in self.items.all():
            total_saved+=cart_item.amount_saved()
        return total_saved
class Address(models.Model):
    user=models.ForeignKey(MyUser,on_delete=models.CASCADE)
    street_address=models.CharField(max_length=255,null=True,blank=True)
    address_type=models.CharField(max_length=255,choices=ADDRESS_CHOICES,null=True)
    def __str__(self):
        return f"{self.user.first_name } {self.user.last_name}"
