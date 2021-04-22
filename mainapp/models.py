from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from .choices import *
from django.conf import settings

# Create your models here.



class ContactForm(models.Model): 
    name = models.CharField(max_length=50,null=True,blank=True)
    email=models.EmailField(max_length=254,blank=True)
    Subject = models.CharField(max_length=200,null=True,blank=True)
    text_message = models.CharField(max_length=1000,null=True,blank=True) 
    created_Entry_date = models.DateTimeField(auto_now=True,editable=False)
     
    



class Product(models.Model):
    title = models.CharField(max_length=130)
    brand = models.CharField(max_length=30,blank=True, null=True,choices=BRANDS,)
    color = models.CharField(max_length=30,blank=True, null=True,choices=COLORS,)

    price = models.IntegerField(null=True,blank=True,)
    size = models.IntegerField(null=True,blank=True,)
    discount_price = models.IntegerField(blank=True, null=True)
    avail_status = models.IntegerField(choices=AVAILABILITY,blank=True,)
    display_info = models.TextField()
    shipping_returns_policy = models.TextField(null=True,blank=True,)
    sale_new_attrib = models.TextField()


    category = models.CharField(choices=CATEGORY_CHOICES, max_length=40)
    date_added = models.DateTimeField(auto_now=True, blank=True, null=True)
    Product_id = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return "%s:%s " % (self.Product_id,self.title)


  


class ImgPath(models.Model):
    capture_value = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    Product_id = models.IntegerField(unique =True,blank=True, null=True)

    path1 = models.CharField(max_length=130)
    path2 = models.CharField(max_length=130)
    path3 = models.CharField(max_length=130)
    path4 = models.CharField(max_length=130)
    thumbpath1 = models.CharField(max_length=130)
    thumbpath2 = models.CharField(max_length=130)
    thumbpath3 = models.CharField(max_length=130)
    thumbpath4 = models.CharField(max_length=130)
    related_product_path_1 = models.CharField(max_length=130)
    related_product_path_2 = models.CharField(max_length=130)
    related_product_path_3 = models.CharField(max_length=130)
    related_product_path_4 = models.CharField(max_length=130)
    related_product_path_5 = models.CharField(max_length=130)

    
    def __str__(self):
        return "%s" % (self.Product_id,)




   


class PincodeCheck(models.Model):
    pincode = models.IntegerField(validators=[MinLengthValidator(6)])
    can_send = models.CharField(max_length=50,null=True,blank=True)
    



class Cart(models.Model):
    username = models.CharField(max_length=50,null=True,blank=True)
    total_price = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)


    title = models.CharField(max_length=130,blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    discount_price = models.IntegerField(blank=True, null=True)
    Product_id = models.IntegerField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now=True,editable=False)


    def __str__(self):
        return self.title


class cartpage_info(models.Model):
    username = models.CharField(max_length=5000,null=True,blank=True)
    orderid = models.BigIntegerField(blank=True, null=True,)
    chargevalue = models.FloatField(null=True,blank=True)


 

      

class Order(models.Model):
    username = models.CharField(max_length=500,null=True,blank=True)
    Address = models.CharField(max_length=200,null=True,blank=True)
    landmark = models.CharField(max_length=200,blank=True, null=True)
    locality = models.CharField(max_length=500,blank=True, null=True)
    city = models.CharField(max_length=20,blank=True, null=True)

    state = models.CharField(max_length=200,blank=True, null=True)
    country = models.CharField(max_length=200,blank=True, null=True)
    payment_mode = models.CharField(max_length=300,blank=True, null=True)

    zipcode = models.CharField(max_length=500,null=True,blank=True)
    mobileno = models.CharField(max_length=50,null=True,blank=True)
    alt_mobileno = models.CharField(max_length=50,null=True,blank=True)


    orderid = models.BigIntegerField(blank=True, null=True,)
    Product_id = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=130,blank=True, null=True)
    discount_price = models.IntegerField(blank=True, null=True)
    gst_added_price = models.FloatField(blank=True, null=True)


    total_price = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    process_status = models.BooleanField(blank =True,null =True,default = 0)
    tracking_status = models.CharField(max_length = 100,null= True,blank=True,choices=TRACKING,default=TRACKING[0][0])


    date_added = models.DateTimeField(auto_now=True,editable=False)



class order2(models.Model):
    username = models.CharField(max_length=500,null=True,blank=True)
    Address = models.CharField(max_length=200,null=True,blank=True)
    city = models.CharField(max_length=200,blank=True, null=True)
    landmark = models.CharField(max_length=200,blank=True, null=True)
    locality = models.CharField(max_length=200,blank=True, null=True)
    state = models.CharField(max_length=200,blank=True, null=True)
    country = models.CharField(max_length=200,blank=True, null=True)
    payment_mode = models.CharField(max_length=300,blank=True, null=True)

    zipcode = models.CharField(max_length=500,null=True,blank=True)
    mobileno = models.CharField(max_length=500,null=True,blank=True)
    alt_mobileno = models.CharField(max_length=500,null=True,blank=True)

    date_added = models.DateTimeField(auto_now=True,editable=False)


    def __str__(self):
        return self.username




class filterinfo(models.Model):
    username = models.CharField(max_length=50,null=True,blank=True)
    category_call = models.TextField(max_length=200,null=True,blank=True,)
    price_call = models.TextField(max_length=200,null=True,blank=True,)
    color_call = models.TextField(max_length=200,null=True,blank=True,)
    brand_call = models.TextField(max_length=200,null=True,blank=True,)
    size_call = models.TextField(max_length=200,null=True,blank=True,)




    date_added = models.DateTimeField(auto_now=True,editable=False)


    def __str__(self):
        return self.username




class searchinfo(models.Model):
    std_search_term = models.TextField(max_length=200,null=True,blank=True,)
    





class searchinfo_by_user(models.Model):
    username = models.CharField(max_length=50,null=True,blank=True)
    search_req = models.TextField(max_length=200,null=True,blank=True,)
    

    date_added = models.DateTimeField(auto_now=True,editable=False)


    def __str__(self):
        return self.username



class TransactionDetails(models.Model):
    trxn_entry = models.CharField(max_length=5000)
  
    date_added = models.DateTimeField(auto_now_add=True,editable=False)

    