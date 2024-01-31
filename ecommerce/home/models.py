from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class GlobalDiscount(models.Model):
    percentage = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.percentage}% Discount"

class Product(models.Model):
    product_id = models.AutoField(primary_key=True, default=1)
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=300)
    pub_date = models.DateField()
    global_discount = models.ForeignKey(GlobalDiscount, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='shop/images', default="")
    
    @property
    def discounted_price(self):
        if self.global_discount:
            discount_percentage = self.global_discount.percentage
            discounted_price = self.price * (1 - (discount_percentage / 100))
            return int(discounted_price)
        else:
            return int(self.price)

    def __str__(self):
        return self.product_name



class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True, default=1)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=70, default="")
    desc = models.CharField(max_length=500, default="")


    def __str__(self):
        return self.name

class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json =  models.CharField(max_length=5000)
    
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=90)
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    amountpaid=models.CharField(max_length=500,blank=True,null=True)
    paymentstatus=models.CharField(max_length=20,blank=True)
    phone = models.CharField(max_length=100,default="")
    complete = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return self.name
    


class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Orders, on_delete=models.CASCADE)
    update_desc = models.CharField(max_length=5000)
    time = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.update_desc[0:7] + "..."

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null = True)

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name}"