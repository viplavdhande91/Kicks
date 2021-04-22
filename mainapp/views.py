from django.shortcuts import render,redirect
from .models import *
import pandas as pd
# Create your views here.
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
import re
import itertools as it
import re

from django.http import JsonResponse
import numpy as np
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from functools import reduce

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

#EMAIL IMPORTS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from smtplib import SMTP
import sys
import itertools

from django.views.decorators.csrf import csrf_exempt
from paytm import Checksum
# Create your views here.

MERCHANT_KEY = 'eeeurfnjvdvJyhrvrve'



def index(request):

 


  user = User();
  if user.is_authenticated:
#CART CHECK FILL VALUE DYNAMICALLY
    cartfiltertable=Cart.objects.all().values_list('quantity').filter(Q(username=request.user.username) )
    df = pd.DataFrame(cartfiltertable, columns=['quantity',])



    df=df.sum(axis = 0, skipna = True) 
      
    recentcartcount =int(df.quantity)
    
    context = {'recentcartcount': recentcartcount,
              }


  return render(request, 'index.html',context)
    
from django.core.paginator import Paginator


def category_main(request,newContext={}):
  paginate_by = 3

  user = User();
  #context.update(newContext)

  if user.is_authenticated:

#CART CHECK FILL VALUE DYNAMICALLY
    cartfiltertable=Cart.objects.all().values_list('quantity').filter(Q(username=request.user.username) )
    df = pd.DataFrame(cartfiltertable, columns=['quantity',])

    df=df.sum(axis = 0, skipna = True) 
      
    recentcartcount =int(df.quantity)
####################################################################333333
    
#EXTRACTING MULTIPLE PRODUCT IMAGES PATH
                
    Image_Path_filtertable=ImgPath.objects.all().values_list('path1','Product_id')
    dfimg = pd.DataFrame(Image_Path_filtertable, columns=['path1','Product_id'])

###price extraction logic
   
    sublist_price  = newContext.get('sublist_price')
    sublist_size = newContext.get('sublist_size')
    sublist_color =newContext.get('sublist_color')
    sublist_brand = newContext.get('sublist_brand')
    sublist_categ =newContext.get('sublist_categ')
    

    if (sublist_price is None) and (sublist_size is None) and (sublist_color is None) and (sublist_brand is None) and  (sublist_categ is None) :
      Product_filtertable=Product.objects.all().values_list('Product_id','title','discount_price',)
      dfproduct = pd.DataFrame(Product_filtertable, columns=['Product_id','title','discount_price',])
      atleast_one = 0
    
    if(bool(newContext)):
      sublist_price  = newContext.get('sublist_price')
      if(sublist_price):
      
      
        flat_list_new_price = list(map(int, it.chain.from_iterable(sublist_price)))    ##list of list to plain list

        flat_list_new_price.sort()
        minprice =flat_list_new_price[0] 
        maxprice= flat_list_new_price[len(flat_list_new_price)-1]
      else:
        minprice =0
        maxprice=0
      

      sublist_len= [len(sublist_price),len(sublist_size),len(sublist_color),len(sublist_brand),len(sublist_categ)]

      atleast_one = 0

      for x in range(len(sublist_len)):
        temp = sublist_len[x]
        if temp!=0:
          atleast_one+=1


      if atleast_one == 1:
        Product_filtertable=Product.objects.all().values_list('Product_id','title','discount_price','color','brand','category','size').filter(Q(discount_price__gte=minprice,discount_price__lte=maxprice) | Q(category__in=newContext.get('sublist_categ')) |  Q(color__in=newContext.get('sublist_color')) | Q(size__in=newContext.get('sublist_size')) |  Q(brand__in =newContext.get('sublist_brand')))
        dfproduct = pd.DataFrame(Product_filtertable, columns=['Product_id','title','discount_price','color','brand','category','size'])
      else:
        Product_filtertable1 = Product.objects.all().values_list('Product_id','title','discount_price','color','brand','category','size').filter(discount_price__gte=minprice,discount_price__lte=maxprice)              
        Product_filtertable2 = Product.objects.all().values_list('Product_id','title','discount_price','color','brand','category','size').filter(category__in=sublist_categ )
        Product_filtertable3 = Product.objects.all().values_list('Product_id','title','discount_price','color','brand','category','size').filter(color__in=sublist_color)
        Product_filtertable4 = Product.objects.all().values_list('Product_id','title','discount_price','color','brand','category','size').filter(size__in=sublist_size)
        Product_filtertable5 = Product.objects.all().values_list('Product_id','title','discount_price','color','brand','category','size').filter(brand__in =sublist_brand) 


        Product_filtertable = Product_filtertable1 | Product_filtertable2 | Product_filtertable3 |Product_filtertable4 | Product_filtertable5
        dfproduct = pd.DataFrame(Product_filtertable, columns=['Product_id','title','discount_price','color','brand','category','size'])



###################check which list is empty and which is filled
        
        if len(sublist_color) == 0:
          sublist_color_isempty = True
        else:
          sublist_color_isempty = False
        


        if len(sublist_brand) == 0:
          sublist_brand_isempty = True
        else:
          sublist_brand_isempty = False
        


        if len(sublist_categ) == 0:
          sublist_categ_isempty = True
        else:
          sublist_categ_isempty = False
        
        if len(sublist_size) == 0:
          sublist_sublist_size = True
        else:
          sublist_sublist_size = False
        

###################filtration proc /Actual ANDing
       

        
        if(sublist_color_isempty ==False):
          dfproduct = dfproduct[np.isin(dfproduct['color'], sublist_color)] 
        
        if(sublist_brand_isempty ==False):
          dfproduct =dfproduct[np.isin(dfproduct['brand'], sublist_brand)]  


        if(sublist_categ_isempty ==False):
          dfproduct =dfproduct[np.isin(dfproduct['category'], sublist_categ)]


        if(sublist_sublist_size ==False):
          dfproduct =dfproduct[np.isin(dfproduct['size'], sublist_size)]

     
        #df01 = dfproduct.to_html(classes=["table-bordered",])


#EXTRACTING MULTIPLE PRODUCT ATTRIBUTES
   
    
    df01 = dfproduct.to_html(classes=["table-bordered",])


 
    df01 = reduce(lambda x,y: pd.merge(x,y, on=['Product_id',], how='outer'), [dfproduct, dfimg])


    df01 = df01.drop_duplicates()    #dropping duplicate rows

    df01 = df01.dropna()         #dropping all null values

    df01['discount_price'] = df01['discount_price'].astype(np.int64)


    df01 = df01.drop_duplicates(subset=['Product_id',], keep='first')

    if(bool(newContext)):
      df01 = df01[['Product_id','title','discount_price','path1','color','brand','category','size']]


 
        
    finalds = df01.to_numpy().tolist() 
    finalds = 16*finalds


     
    df01 = df01.to_html(classes=["table-bordered",])
   
 

    paginator = Paginator(finalds, 24) # Show 24 contacts per page.
    page = request.GET.get('page')
    finalds = paginator.get_page(page)



    context = {'recentcartcount': recentcartcount,
               'finalds':finalds,
               'df01':df01,
               'newContext':newContext,

              
               'atleast_one':atleast_one,


              }
    context.update(newContext) 
 
 


  return render(request,'category.html',context,)




def category_filter(request):

  user = User();
#########FILTER REMOVAL USECASE
  if user.is_authenticated and request.is_ajax() and request.method == 'GET' :
    category_call = request.GET.get('category_call')
    price_call = request.GET.get('price_call')
    color_call = request.GET.get('color_call')
    brand_call = request.GET.get('brand_call')
    size_call = request.GET.get('size_call')




    objfilterinfo = filterinfo(username=request.user.username,category_call=category_call,price_call=price_call,color_call=color_call,brand_call=brand_call,size_call=size_call)
    objfilterinfo.save()


###############CONTExT UPDATE LOGIC
  filterinfo_queryset=filterinfo.objects.all().values_list('username','category_call','price_call','color_call','brand_call','size_call',).filter(Q(username=request.user.username))
  df = pd.DataFrame(filterinfo_queryset, columns=['username','category_call','price_call','color_call','brand_call','size_call',])

      
  dflength = df.size/6
  dflength = int(dflength)
  df= df.dropna(axis='columns', how='all')
  df = df.drop(['username',], axis=1)
  df = df.drop(df.index[0:dflength-1])
  df= df.dropna(axis='columns', how='all')

 
##########list filteration logic start
  actual_list =  df.values.tolist()
#list of list to flat list
  flat_list = []
  for sublist in actual_list:
    for item in sublist:
      flat_list.append(item)

  flat_list[0] = eval(flat_list[0])  #remove more time occuring quotes

  flat_list_new = []
  for sublist in flat_list:
    for item in sublist:
      flat_list_new.append(item)


##########list filteration logic end
  sublist_categ = []
  sublist_price = []
  sublist_color = []
  sublist_size = []
  sublist_brand = []


  
  for i in range(len(flat_list_new)):
    temp = flat_list_new[i]
    if temp == 'sneakers' or temp =='casualshoes' or temp == 'formalshoes' or temp == 'studds':
      sublist_categ.append(temp)

   
    if temp == 'Rs.112 to Rs.999' or temp =='Rs.1000 to Rs.2147' or temp =='Rs.2148 to Rs.5487' or temp =='Rs.5488 to Rs.9457':

      temp = temp.replace('Rs.','')
      temp = temp.replace('to ','')
      temp = temp.split()
      for x in range(len(temp)):
        temp_0 = temp[x]
        temp[x] = int(temp_0)
      sublist_price.append(temp)
    
    if temp == 'turquoise' or temp =='gray' or temp =='orange' or temp =='yellow' or temp =='green' or temp =='purple' or temp =='blue':
      sublist_color.append(temp)

    
    if temp  =='6' or temp =='7' or temp =='8' or temp =='9' or temp =='10' or temp =='11':
      sublist_size.append(int(temp))

    
    if temp == 'nike' or temp =='puma' or temp =='addidas' or temp =='sketchers':
      sublist_brand.append(temp)

  
  
  finalwrap = [sublist_categ,sublist_price,sublist_color,sublist_size,sublist_brand]
################IF FILTERATION CONTEXT GET UPDATED#########
 





##############CHECKBOX SETTERS
#####1)CATEGORY LIST
  if "sneakers" in sublist_categ:
    checkbox_sneakers = True
  else:
    checkbox_sneakers = False

  if "casualshoes" in sublist_categ:
    checkbox_casualshoes = True
  else:
    checkbox_casualshoes = False

  if "formalshoes" in sublist_categ:
    checkbox_formalshoes = True
  else:
    checkbox_formalshoes = False

  if "studds" in sublist_categ:
    checkbox_studds = True
  else:
    checkbox_studds = False
#####2)PRICE


  if [112,999] in sublist_price:
    checkbox_price1 = True
  else:
    checkbox_price1 = False

  if [1000,2147] in sublist_price:
    checkbox_price2 = True
  else:
    checkbox_price2 = False

  if [2148,5487] in sublist_price:
    checkbox_price3 = True
  else:
    checkbox_price3 = False

  if [5488,9457] in sublist_price:
    checkbox_price4 = True
  else:
    checkbox_price4 = False


############3)color
  if "turquoise" in sublist_color:
    checkbox_turquoise = True
  else:
    checkbox_turquoise = False

  if "gray" in sublist_color:
    checkbox_gray = True
  else:
    checkbox_gray = False

  if "orange" in sublist_color:
    checkbox_orange = True
  else:
    checkbox_orange = False

  if "green" in sublist_color:
    checkbox_green = True
  else:
    checkbox_green = False

  if "purple" in sublist_color:
    checkbox_purple = True
  else:
    checkbox_purple = False

  if "blue" in sublist_color:
    checkbox_blue = True
  else:
    checkbox_blue = False
  if "yellow" in sublist_color:
    checkbox_yellow = True
  else:
    checkbox_yellow = False






############4)size
  if 6 in sublist_size:
    checkbox_six = True
  else:
    checkbox_six = False

  if 7 in sublist_size:
    checkbox_seven = True
  else:
    checkbox_seven = False

  if 8 in sublist_size:
    checkbox_eight = True
  else:
    checkbox_eight = False

  if 9 in sublist_size:
    checkbox_nine = True
  else:
    checkbox_nine = False

  if 10 in sublist_size:
    checkbox_ten = True
  else:
    checkbox_ten = False

  if 11 in sublist_size:
    checkbox_eleven = True
  else:
    checkbox_eleven = False
 




############5)brand
  if "nike" in sublist_brand:
    checkbox_nike = True
  else:
    checkbox_nike = False

  if "puma" in sublist_brand:
    checkbox_puma = True
  else:
    checkbox_puma = False

  if "addidas" in sublist_brand:
    checkbox_addidas = True
  else:
    checkbox_addidas = False

  if "sketchers" in sublist_brand:
    checkbox_sketchers = True
  else:
    checkbox_sketchers = False

 







  df02 = df.to_html(classes=["table-bordered",])

####################################################################3333


  context = {'flat_list_new': flat_list_new,
  'dflength':dflength,
  'df02':df02,
  'finalwrap':finalwrap,
  'sublist_categ':sublist_categ,
  'sublist_price':sublist_price,
  'sublist_color':sublist_color,
  'sublist_size':sublist_size,
  'sublist_brand':sublist_brand,
  
  'checkbox_sneakers':checkbox_sneakers,
  'checkbox_casualshoes':checkbox_casualshoes,
  'checkbox_formalshoes':checkbox_formalshoes,
  'checkbox_studds':checkbox_studds,
  
  'checkbox_price1':checkbox_price1,
  'checkbox_price2':checkbox_price2,
  'checkbox_price3':checkbox_price3,
  'checkbox_price4':checkbox_price4,

  'checkbox_turquoise':checkbox_turquoise,
  'checkbox_gray':checkbox_gray,
  'checkbox_orange':checkbox_orange,
  'checkbox_green':checkbox_green,
  'checkbox_purple':checkbox_purple,
  'checkbox_blue':checkbox_blue,
  'checkbox_yellow':checkbox_yellow,


  'checkbox_six':checkbox_six,
  'checkbox_seven':checkbox_seven,
  'checkbox_eight' :checkbox_eight,
  'checkbox_nine' :checkbox_nine,
  'checkbox_ten':checkbox_ten,
  'checkbox_eleven':checkbox_eleven,


  'checkbox_nike':checkbox_nike,
  'checkbox_puma':checkbox_puma,
  'checkbox_addidas':checkbox_addidas,
  'checkbox_sketchers':checkbox_sketchers,

  
              }



  response = category_main(request,context)
  return response
  #return render(request,'test.html',context)







def category_filter_delete(request,filterval):
  user = User();

  if user.is_authenticated:
    entry =filterinfo.objects.order_by('username', 'date_added').values_list('username','category_call','price_call','color_call','brand_call','size_call',).filter(Q(username=request.user.username)).last() 
    entry = list(entry)
    

    while None in entry:
      entry.remove(None)
    entry.remove(request.user.username)

    entry = re.findall(r'\w+', entry[0])

    entry.remove(filterval)


    objfilterinfo = filterinfo(username=request.user.username,category_call=entry)
    objfilterinfo.save()


    if len(entry)==0:
      return redirect('/category_main/')

    else:
      return redirect('/category_filter/')






def search_term(request):
 
        
  if request.method =='POST':
    search_req= request.POST.get('search_contains')

    if search_req!= '':
      objsearchinfo_by_user = searchinfo_by_user(username=request.user.username, search_req=search_req,)
      objsearchinfo_by_user.save()


    search_req = re.findall(r'\w+', search_req) #cuts string and collects string on empty space seperator

    objfilterinfo =filterinfo(username=request.user.username,price_call =search_req ) 
    objfilterinfo.save()

    return redirect('/category_filter/')

    

  if(request.is_ajax()):

    search_term = request.GET.get('search_param')

    captured_qs = searchinfo.objects.values_list('std_search_term').filter(Q(std_search_term__icontains= search_term))
    df = pd.DataFrame(captured_qs, columns=['std_search_term',])

    captured_qs =  df.to_numpy().tolist() 

    captured_qs = list(map(str, it.chain.from_iterable(captured_qs)))    ##list of list to plain list
     
   
           
    data = {
              'is_present' : True,
              'captured_qs': captured_qs,
                  }



    return JsonResponse(data, safe=False,)
    


import datetime 
import random as rd
import uuid


def coupon_apply(request):    
  if request.is_ajax() and request.method == 'GET':
    seq = request.GET.get('orderid_random')
    seq = int(seq) 
   

    objcartapage_info = cartpage_info(username=request.user.username, orderid=seq)
    objcartapage_info.save()




     
  
     
              
    data = {
              'is_present' : True,
                  }



    return JsonResponse(data, safe=False,)
    





def Contact(request):
    user = User();
    if user.is_authenticated:
#CART CHECK FILL VALUE DYNAMICALLY
      cartfiltertable=Cart.objects.all().values_list('quantity').filter(Q(username=request.user.username) )
      df = pd.DataFrame(cartfiltertable, columns=['quantity',])

      df=df.sum(axis = 0, skipna = True) 
      
      recentcartcount =int(df.quantity)
    
      context = {'recentcartcount': recentcartcount,
              }
      return render(request,'contact.html',context)




def ContactFormRecieved(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['e_mail']
        Subject = request.POST['Subject_of_discuss']
        text_message = request.POST['message_typed']


        objcontact = ContactForm(name=name, email=email, Subject=Subject,text_message =text_message)
        objcontact.save()
        
    return render(request,'index.html')


def productinfo(request,itemid):
    pd.set_option('display.max_colwidth', -1)
    if request.method == 'GET':
################################ PRODUCT STATIC INFO TRANSFER FROM DB TO HTML TEMPLATE
        Productfiltertable=Product.objects.all().values_list('title','brand','price','size','discount_price','avail_status','display_info','shipping_returns_policy','category','Product_id').filter(Product_id = itemid )
        df = pd.DataFrame(Productfiltertable, columns=['title','brand','price','size','discount_price','avail_status','display_info','shipping_returns_policy','category','Product_id'])

        producttitle = df['title'][0]
        product_price =df['price'][0]
        product_discount_price =df['discount_price'][0]
        product_avail_status = df['avail_status'][0]
    
        product_display_info = df['display_info'][0]
        product_shipping_returns_policy =df['shipping_returns_policy'][0]
        product_brand =df['brand'][0]


        product_id_df_var =df['Product_id'][0]

#######################################PERCENTAGE CALCULATOR 
        perc1 = (product_discount_price/product_price)*100
        perc1 =100 - int(round(perc1))




#######################################SIZE BUTTON ACTIVE DEACTIVE LOGIC
        SmallProductfiltertable=Product.objects.all().values_list('size','avail_status').filter(Q(avail_status = 0) & Q(Product_id =itemid))

        df_but_act_logic = pd.DataFrame(SmallProductfiltertable, columns=['size','avail_status'])

       

        outofstockitemlist = df_but_act_logic['size'].tolist()

        size6var = 1
        size7var = 1
        size8var = 1
        size9var = 1
        size10var = 1
        size11var = 1

        for x in range(len(outofstockitemlist)):
          temp =outofstockitemlist[x]
          

          if temp == 6:                 
            size6var = False
          else:
            if size6var == 1:
              size6var = True
            else:
              size6var = False

          if temp == 7:
            size7var = False
          else:
            if size7var == 1:
              size7var = True
            else:
              size7var =False


          if temp == 8:
            size8var = False
          else:

            if size8var == 1:
              size8var =True
            else:
              size8var =False



          if temp == 9:
            size9var = False
          else:

            if size9var == 1:
              size9var =True
            else:
              size9var =False





          if temp == 10:
            size10var = False
          else:

            if size10var == 1:
              size10var =True
            else:
              size10var =False



          if temp == 11:
            size11var = False
          else:

            if size11var == 1:
              size11var =True
            else:
              size11var =False

            
                    
        testvar =outofstockitemlist
      
             

######################## PRODUCT IMAGES PATH TRANSFER FROM DB TO HTML
        Image_Path_filtertable=ImgPath.objects.all().values_list('path1','path2','path3','path4','thumbpath1','thumbpath2','thumbpath3','thumbpath4','related_product_path_1','related_product_path_2','related_product_path_3','related_product_path_4','related_product_path_5',).filter(Product_id = itemid )
        df1 = pd.DataFrame(Image_Path_filtertable, columns=['path1','path2','path3','path4','thumbpath1','thumbpath2','thumbpath3','thumbpath4','related_product_path_1','related_product_path_2','related_product_path_3','related_product_path_4','related_product_path_5',])

        image_path1 = df1['path1'][0]
        
        image_path2 = df1['path2'][0]

        image_path3 = df1['path3'][0]

        image_path4 = df1['path4'][0]

        image_thumbpath1 = df1['thumbpath1'][0]
        
        image_thumbpath2 = df1['thumbpath2'][0]

        image_thumbpath3 = df1['thumbpath3'][0]

        image_thumbpath4 = df1['thumbpath4'][0]

        image_related_product_path_1 = df1['related_product_path_1'][0]
        
        image_related_product_path_2 = df1['related_product_path_2'][0]

        image_related_product_path_3 = df1['related_product_path_3'][0]

        image_related_product_path_4 = df1['related_product_path_4'][0]

        image_related_product_path_5 = df1['related_product_path_5'][0]


#CART DISPLAY FILL VALUE DYNAMICALLY
        cartfiltertable=Cart.objects.all().values_list('quantity').filter(Q(username=request.user.username) )
        sdf = pd.DataFrame(cartfiltertable, columns=['quantity',])

        sdf=sdf.sum(axis = 0, skipna = True) 
      
        recentcartcount =int(sdf.quantity)
    
     
###############################
        cartfiltertable=Cart.objects.all().values_list('Product_id','size').filter(username=request.user.username)
        df2 = pd.DataFrame(cartfiltertable, columns=['Product_id','size'])
        
        
        #cartcount =int(df2.size/ 2)  #here .size is pandas df length attribute and it returns all present element count
 
        productlist = list(df2.Product_id)
        

        product_add_kiya_hai = itemid in productlist

        if product_add_kiya_hai== True:
          passvar = 1
        else:
          passvar = 0
          
                    

        context = {'producttitle': producttitle,
        'product_price': product_price,
        'product_discount_price': product_discount_price,
        'product_avail_status': product_avail_status,
        'product_display_info': product_display_info,
        'product_shipping_returns_policy': product_shipping_returns_policy,
         'image_path1': image_path1,
         'image_path2': image_path2,
         'image_path3': image_path3,
         'image_path4': image_path4,
          'image_thumbpath1': image_thumbpath1,
          'image_thumbpath2': image_thumbpath2,

          'image_thumbpath3': image_thumbpath3,

          'image_thumbpath4': image_thumbpath4,
          'image_related_product_path_1': image_related_product_path_1,
          'image_related_product_path_2': image_related_product_path_2,

          'image_related_product_path_3': image_related_product_path_3,

          'image_related_product_path_4': image_related_product_path_4,

          'image_related_product_path_5': image_related_product_path_5,
          'recentcartcount': recentcartcount,
          'product_add_kiya_hai' :product_add_kiya_hai,
          'itemid':itemid,
          'product_brand':product_brand,
          'perc1':perc1,
          'passvar':passvar,
          'SmallProductfiltertable':SmallProductfiltertable,
           'size6var':size6var,
           'size7var':size7var,
           'size8var':size8var,
           'size9var':size9var,
           'size10var':size10var,
           'size11var':size11var,
           'testvar' :testvar,



          }

        return render(request,'product.html',context= context)




@csrf_exempt
def signup(request):
    if request.is_ajax() and request.method == 'GET':
      username = request.GET.get('username')
      email = request.GET.get('email')


      val =[[101, 'Men Red SF Roma Sneakers', 5499, 'img/all_products/101/1.jpg'], [102, 'ADDIDAS TURQUOISE SHOES', 4524, 'img/all_products/102/1.jpg']]
      data = {
        'is_taken': User.objects.filter(username__iexact=username).exists(),
         'is_taken_em': User.objects.filter(email__iexact=email).exists(),

        'datasend' :val}


      return JsonResponse(data)

    if request.method == 'POST':
        usernamecapture = request.POST['username']
        emailcapture = request.POST['emailinp']
        firstnamecapture = request.POST['firstname']
        lastnamecapture = request.POST['lastname']
        passwordcapture = request.POST['signuppassword']



        user = User(username=usernamecapture, email=emailcapture, first_name =firstnamecapture ,last_name =lastnamecapture,is_staff=True,is_superuser =False)
        user.set_password(passwordcapture)
        user.save()
        return render(request, 'registration/thankyou_reg.html')
    else:
        return render(request, 'registration/signup.html')




    


@csrf_exempt
def view_login(request):
    if request.method == "POST":
        user_name = request.POST.get("username",)
        pass_word = request.POST.get("pass",)
        user = authenticate(request,username=user_name,password=pass_word)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
          msginfo = 'You have entered Wrong UserId/Password.Kindly Enter Valid Credentials'
          status = True
          context = {'msginfo':msginfo,
          'status':status
          }
          return render(request, 'registration/login.html',context)

    elif request.method == "GET":
        return render(request,"registration/login.html",{})



def view_logout(request):
    logout(request)
    return redirect('/')











def add_to_cart(request):
    if request.is_ajax():

      title1 = request.GET.get('title')
      product_price1 = request.GET.get('product_price')
      product_discount_price1 = request.GET.get('product_discount_price')
      Product_id1 = request.GET.get('Product_id')
      username1 = request.GET.get('username')
      size1 = request.GET.get('size')
      quantity1 =request.GET.get('quantity') 
      total = int(product_discount_price1) * int(quantity1)

      objcart = Cart(title=title1,Product_id= Product_id1,quantity = quantity1 ,total_price = total,price = product_price1,size =size1,discount_price = product_discount_price1,username=username1)
      objcart.save()


# CART DISPLAY FILL VALUE DYNAMICALLY

      cartfiltertable=Cart.objects.all().values_list('quantity').filter(Q(username=request.user.username) )
      df = pd.DataFrame(cartfiltertable, columns=['quantity',])


      df=df.sum(axis = 0, skipna = True) 
      
      recentcartcount =int(df.quantity)

             
      data = {'recentcartcount' : recentcartcount,
                  'is_present1' : True,}



      return JsonResponse(data ,safe=False)





def delete_from_cart(request,itemid):

  Product_id1 = itemid

  Cart.objects.filter(Q(username=request.user.username) & Q(Product_id=Product_id1)).delete()

  return redirect('/cartpage/')









def cartpage(request):
    user = User();
    if user.is_authenticated:

# CART DISPLAY FILL VALUE DYNAMICALLY
      cartfiltertable=Cart.objects.all().values_list('quantity').filter(Q(username=request.user.username) )
      df = pd.DataFrame(cartfiltertable, columns=['quantity',])
      df=df.sum(axis = 0, skipna = True) 

      recentcartcount =int(df.quantity)   

#############################################
      Cart_sucked=Cart.objects.all().values_list('Product_id','discount_price','quantity').filter(username=request.user.username)
      df1 = pd.DataFrame(Cart_sucked, columns=['Product_id','discount_price','quantity',])

      df1['discount_price'] = df1['discount_price']*df1['quantity']

      df1 = df1.drop(['Product_id','quantity'], axis=1)
           
      
      df1=df1.sum(axis = 0, skipna = True)

      cart_sum = int(df1.discount_price)
      

      shipping_charges = 'FREE'
      tax = "18"+'%'+"GST"

      
      final_sum = cart_sum +(cart_sum * 0.18)


  


#CART CHECK FILL VALUE DYNAMICALLY &EXTRACTING PRODUCT DETAILS

      indextotalsucked=Cart.objects.all().values_list('Product_id','title','discount_price','size','quantity',).filter(username=request.user.username)
      df00 = pd.DataFrame(indextotalsucked, columns=['Product_id','title','discount_price','size','quantity'])

    



      if(df.empty == True):
        cart_empty_hai_kya = True
      else:
        cart_empty_hai_kya = False
         


#EXTRACTING MULTIPLE PRODUCT IMAGES PATH
                
      Image_Path_filtertable=ImgPath.objects.all().values_list('path1','Product_id')
      df01 = pd.DataFrame(Image_Path_filtertable, columns=['path1','Product_id'])



#EXTRACTING MULTIPLE PRODUCT ATTRIBUTES
                
      Product_filtertable=Product.objects.all().values_list('Product_id','category','category')
      df02 = pd.DataFrame(Product_filtertable, columns=['Product_id','category','category'])






      df01 = reduce(lambda x,y: pd.merge(x,y, on=['Product_id',], how='outer'), [df01, df00])

      df02 = reduce(lambda x,y: pd.merge(x,y, on=['Product_id',], how='outer'), [df02, df01])

      df02 = df02.drop_duplicates()    #dropping duplicate rows

      df02 = df02.dropna()         #dropping all null values

      df02['discount_price'] = df02['discount_price'].astype(np.int64)
      df02['size'] = df02['size'].astype(np.int64)
      df02['quantity'] = df02['quantity'].astype(np.int64)


      

#creating final  data structure
        
      finalds = df02.to_numpy().tolist()      

      df02 = df02.to_html(classes=["table-bordered",])
      context = {'df02': df02,
             'recentcartcount':recentcartcount,
             'cart_empty_hai_kya':cart_empty_hai_kya,
             'finalds':finalds,
             'cart_sum':cart_sum,
             'final_sum':final_sum,
             'tax':tax,
             'shipping_charges':shipping_charges,
             }




      return render(request,'cart.html',context)



        
         




              
import json


def calculate(request,newContext={}):
  

  verify = newContext.get('verify')

  response_dict = newContext.get('response_dict')

  json_object = json.dumps(response_dict)
 
    

  if verify:
    if response_dict['RESPCODE'] == '01':
      objTransactionDetails = TransactionDetails(trxn_entry = json_object)
      objTransactionDetails.save()
      print('order success')      
    else:
      
      print('order failure')



  return redirect('/orders/order_category_page/')



def delete_from_cart(request,itemid):

  Product_id1 = itemid

  Cart.objects.filter(Q(username=request.user.username) & Q(Product_id=Product_id1)).delete()

  return redirect('/cartpage/')








def checkout(request):
  user = User();
  if user.is_authenticated:

# CART DISPLAY FILL VALUE DYNAMICALLY

    cartfiltertable=Cart.objects.all().values_list('quantity').filter(Q(username=request.user.username) )
    df = pd.DataFrame(cartfiltertable, columns=['quantity',])
    df=df.sum(axis = 0, skipna = True) 

    recentcartcount =int(df.quantity)   

#############################################
    Cart_sucked=Cart.objects.all().values_list('Product_id','discount_price','quantity').filter(username=request.user.username)
    df1 = pd.DataFrame(Cart_sucked, columns=['Product_id','discount_price','quantity',])

    df1['discount_price'] = df1['discount_price']*df1['quantity']

    df1 = df1.drop(['Product_id','quantity'], axis=1)
           
      
    df1=df1.sum(axis = 0, skipna = True)

    cart_sum = int(df1.discount_price)
      





      

    shipping_charges = 'FREE'
    tax = "18"+'%'+"GST"

      
    final_sum = cart_sum +(cart_sum * 0.18)




  


#CART CHECK FILL VALUE DYNAMICALLY &EXTRACTING PRODUCT DETAILS

    indextotalsucked=Cart.objects.all().values_list('Product_id','title','discount_price','size','quantity',).filter(username=request.user.username)
    df00 = pd.DataFrame(indextotalsucked, columns=['Product_id','title','discount_price','size','quantity'])

    



    if(df.empty == True):
      cart_empty_hai_kya = True
    else:
      cart_empty_hai_kya = False
         


#EXTRACTING MULTIPLE PRODUCT IMAGES PATH
                
    Image_Path_filtertable=ImgPath.objects.all().values_list('path1','Product_id')
    df01 = pd.DataFrame(Image_Path_filtertable, columns=['path1','Product_id'])



#EXTRACTING MULTIPLE PRODUCT ATTRIBUTES
                
    Product_filtertable=Product.objects.all().values_list('Product_id','category','category')
    df02 = pd.DataFrame(Product_filtertable, columns=['Product_id','category','category'])






    df01 = reduce(lambda x,y: pd.merge(x,y, on=['Product_id',], how='outer'), [df01, df00])

    df02 = reduce(lambda x,y: pd.merge(x,y, on=['Product_id',], how='outer'), [df02, df01])

    df02 = df02.drop_duplicates()    #dropping duplicate rows

    df02 = df02.dropna()         #dropping all null values

    df02['discount_price'] = df02['discount_price'].astype(np.int64)
    df02['size'] = df02['size'].astype(np.int64)
    df02['quantity'] = df02['quantity'].astype(np.int64)


      

#creating final  data structure
        
    finalds = df02.to_numpy().tolist()      

    df02 = df02.to_html(classes=["table-bordered",])
    context = {'df02': df02,
             'recentcartcount':recentcartcount,
             'cart_empty_hai_kya':cart_empty_hai_kya,
             'finalds':finalds,
             'cart_sum':cart_sum,
             'final_sum':final_sum,
             'tax':tax,
             'shipping_charges':shipping_charges,
             }

 
  
    return render(request, 'checkout.html',context) 





def charge_val_get(request):
  if request.is_ajax():
    amount = request.GET.get('amount')
   # amount = int(amount)

    objcartapage_info = cartpage_info(username=request.user.username,chargevalue =amount )
    objcartapage_info.save()

  



def place_order(request):
  if request.method == 'POST':

    amount = request.GET.get('amount')
     
    adress11 = request.POST.get('addr1')
    landmark11= request.POST.get('landmark1')
    locality11= request.POST.get('locality')

    city11 =  request.POST.get('city')


    payment_mode =request.POST.get('ship-22')

    state11= request.POST.get('stateofuser')
    zip_code11 = request.POST.get('zip_code')
    mobile_no11 = request.POST.get('phone_no')

    alt_mobileno11 = request.POST.get('alt_phone_no')

    country11= request.POST.get('country_id')

    confirm_consent =  request.POST.get('confirm',)
    confirm_consent = int(confirm_consent)

    if landmark11 == "" :
      landmark11 = '-'

    if locality11 == "":
      locality11 ='-'

    if alt_mobileno11 == "":
      alt_mobileno11 ='-'



    

    objorder2 = order2(username=request.user.username,Address =adress11 ,payment_mode = payment_mode ,landmark = landmark11 ,alt_mobileno = alt_mobileno11,locality = locality11,city =city11 ,state = state11 ,country =country11,zipcode =zip_code11,mobileno =mobile_no11)
    objorder2.save()
   

    Cart_sucked_qs=Cart.objects.all().values_list('username','Product_id','title','discount_price','total_price','size','quantity',).filter(username=request.user.username)
    df000 = pd.DataFrame(Cart_sucked_qs, columns=['username','Product_id','title','discount_price','total_price','size','quantity'])



 


                
    orderid_qs=cartpage_info.objects.all().values_list('username','orderid','chargevalue').filter(username=request.user.username)
    df011 = pd.DataFrame(orderid_qs, columns=['username','orderid','chargevalue'])


    recentorderid_list = df011['orderid'].dropna().unique().tolist()
    recentorderid_list = list(map(round, recentorderid_list))


    recentchargevalue_list = df011['chargevalue'].dropna().unique().tolist()


    recentorderid = recentorderid_list[0]
    amount = recentchargevalue_list[0]


    df011 = df011.fillna(0) #REPLACE ALL VALUES OF NAN TO 0







                
    order2_qs=order2.objects.all().values_list('username','Address','landmark','locality','city','state','country','payment_mode','zipcode', 'mobileno','alt_mobileno',).filter(username=request.user.username)
    df022 = pd.DataFrame(order2_qs, columns=['username','Address','landmark','locality','city','state','country','payment_mode','zipcode', 'mobileno','alt_mobileno',])






    df011 = reduce(lambda x,y: pd.merge(x,y, on=['username',], how='outer'), [df011, df000])

    df022 = reduce(lambda x,y: pd.merge(x,y, on=['username',], how='outer'), [df022, df011])

    df022 = df022.drop_duplicates()    #dropping duplicate rows


    df022 = df022.dropna()         #dropping all null values

    df022 = df022.drop(df022[(df022['orderid'] == 0.0) ].index)

    dfcap  = df022


    df022['discount_price'] = df022['discount_price'].astype(np.int64)
    df022['size'] = df022['size'].astype(np.int64)
    df022['quantity'] = df022['quantity'].astype(np.int64)
    df022['total_price'] = df022['total_price'].astype(np.int64)

    df022 = df022[['username','Address','landmark','locality','city','state','country','payment_mode','zipcode','mobileno','alt_mobileno','orderid','Product_id','title','discount_price','total_price','size','quantity','chargevalue']]

    listtosave = df022.to_numpy().tolist()      


    for x in range(len(listtosave)):

      objorder = Order(username=listtosave[x][0],Address =listtosave[x][1] ,gst_added_price=amount, landmark = listtosave[x][2] ,locality = listtosave[x][3] ,city = listtosave[x][4],state = listtosave[x][5],country =listtosave[x][6] ,payment_mode =listtosave[x][7],zipcode =listtosave[x][8],mobileno =listtosave[x][9],alt_mobileno=listtosave[x][10],orderid=listtosave[x][11],Product_id =listtosave[x][12],title=listtosave[x][13],discount_price =listtosave[x][14],total_price =listtosave[x][15],size = listtosave[x][16],quantity = listtosave[x][17])
      objorder.save()



    dfcap = dfcap.to_html(classes=["table-bordered",])




    Cart.objects.filter(username=request.user.username).delete()

    cartpage_info.objects.filter(username=request.user.username).delete()

    order2.objects.filter(username=request.user.username).delete()



    
    
    emailsend(request,recentorderid)


    Order_sucked_qs=Order.objects.all().values_list('username','payment_mode','orderid','total_price',).filter(Q(username=request.user.username) & Q(orderid = recentorderid) &Q(payment_mode ='OnlinePayment'))
    df0000 = pd.DataFrame(Order_sucked_qs, columns=['username','payment_mode','orderid','total_price',])


  

                     
    if payment_mode=='OnlinePayment':

      param_dict = {

                'MID': 'dvegrfvervvrvrvvvvv96434337',
                'ORDER_ID': str(recentorderid),
                'TXN_AMOUNT': str(amount),
                'CUST_ID': 'demo@paytm.com',
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'https://kicks92.herokuapp.com/handlerequest/',

        }
      param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)

      return render(request, 'payments/paytm.html', {'param_dict': param_dict})

    elif payment_mode == 'CashOnDelivery':
          return render(request,'thankyou.html',{'dfcap':dfcap,'listtosave':listtosave,'recentorderid_list':recentorderid_list,'recentorderid':recentorderid,'amount':amount})


   

   


        



@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
  form = request.POST
  response_dict = {}
  for i in form.keys():
      response_dict[i] = form[i]
      if i == 'CHECKSUMHASH':
        checksum = form[i]

  verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
  
 

      

  context= {'response_dict': response_dict,
                  'verify':verify}

  response = calculate(request,context)

  return response





























def emailsend(request,recentorderid):

  sender_address = 'vpp.19p10242@mtech.nitdgp.ac.in'
  PASSWORD = '*viplavgate012345678#'

  

  user = User()
  ordersend_qs=Order.objects.all().values_list('username','Address','landmark','locality','city','state','country','payment_mode','zipcode','mobileno','alt_mobileno','orderid','Product_id','title','discount_price','total_price','size','quantity',).filter(Q(username=request.user.username) & Q(orderid = recentorderid))
  df_test = pd.DataFrame(ordersend_qs, columns=['username','Address','landmark','locality','city','state','country','payment_mode','zipcode','mobileno','alt_mobileno','orderid','Product_id','title','discount_price','total_price','size','quantity',])

  df_test = df_test.drop_duplicates()    #dropping duplicate rows

  df_test = df_test.dropna()         #dropping all null values

  df_test['Customer_Name'] = request.user.get_full_name()

  df_test = df_test[['Customer_Name','Address','landmark','locality','city','state','country','payment_mode','zipcode','mobileno','alt_mobileno','orderid','Product_id','title','discount_price','total_price','size','quantity',]]


  df_test['size'] = df_test['size'].astype(np.int64)
  df_test['quantity'] = df_test['quantity'].astype(np.int64)
  df_test['Product_id'] = df_test['Product_id'].astype(np.int64)

    
#creating final  data structure
        
  recipients = ['viplavdhande91@gmail.com',] 
  emaillist = [elem.strip().split(',') for elem in recipients]
  msg = MIMEMultipart()
  msg['Subject'] = "✔ Yay! New order recieved on Kicks Online Store"
  msg['From'] = sender_address

  html = """\
        <html>
          <head></head>
          <body>
            <h3>You can Order Entries Admin panel by clicking on below link</h3>

            <p>https://kicks92.herokuapp.com/kicksadminpanel/mainapp/order2/</p>

            {0}
          </body>
          </html>""".format(df_test.to_html(index=False))
   
  part1 = MIMEText(html, 'html')
  msg.attach(part1)


  try:

    server = smtplib.SMTP('smtp.gmail.com', 587)
    #server.ehlo()#NOT NECESSARY
    server.starttls()
    #server.ehlo()#NOT NECESSARY
    server.login(sender_address,PASSWORD)
    server.sendmail(msg['From'], emaillist , msg.as_string())
    server.close()

  except Exception as e:
    print("Error for connection: {}".format(e))


  
      