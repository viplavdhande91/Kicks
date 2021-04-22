from django.shortcuts import render
from django.contrib.auth.models import User
from mainapp.models import *
from django.db.models import Q
import pandas as pd
from functools import reduce
import numpy as np
# Create your views here.




def order_category_page(request):
    user = User();
    if user.is_authenticated:
#CART CHECK FILL VALUE DYNAMICALLY
      cartfiltertable=Cart.objects.all().values_list('quantity').filter(Q(username=request.user.username) )
      df = pd.DataFrame(cartfiltertable, columns=['quantity',])


      df=df.sum(axis = 0, skipna = True) 
      
      recentcartcount =int(df.quantity)
    
      

#############################################
   
      Order_sucked=Order.objects.all().values_list('title','discount_price','orderid','Product_id','total_price','size','quantity','gst_added_price','tracking_status','process_status').filter(username=request.user.username )
      df0 = pd.DataFrame(Order_sucked, columns=['title','discount_price','orderid','Product_id','total_price','size','quantity','gst_added_price','tracking_status','process_status'])


#EXTRACTING MULTIPLE PRODUCT IMAGES PATH
                
      Image_Path_filtertable=ImgPath.objects.all().values_list('path1','Product_id')
      df1 = pd.DataFrame(Image_Path_filtertable, columns=['path1','Product_id'])



#EXTRACTING MULTIPLE PRODUCT ATTRIBUTES
                
      Product_filtertable=Product.objects.all().values_list('Product_id','category',)
      df2= pd.DataFrame(Product_filtertable, columns=['Product_id','category',])



      df1 = reduce(lambda x,y: pd.merge(x,y, on=['Product_id',], how='outer'), [df1, df0])

      df3 = reduce(lambda x,y: pd.merge(x,y, on=['Product_id',], how='outer'), [df2, df1])
      


      df3 = df3.drop_duplicates()    #dropping duplicate rows

      df3 = df3.dropna()         #dropping all null values


     # orderid = int(df3['orderid'][0])

      df3['total_price'] = df3['total_price'].astype(np.int64)
      df3['size'] = df3['size'].astype(np.int64)
      df3['discount_price'] = df3['discount_price'].astype(np.int64)
      df3['quantity'] = df3['quantity'].astype(np.int64)
      df3['orderid'] = df3['orderid'].astype(np.int64)




##############################  VARIOUS VALUES CALCULATIONS
     # orderid = df3['orderid'][0]

      
      total_price =int(df3['total_price'].sum())


      discount = 0

      gstaddsum =(total_price/100)*18 
                
    
      TransactionDetails_qs=TransactionDetails.objects.all().values_list('trxn_entry',)
      dftrxn = pd.DataFrame(TransactionDetails_qs, columns=['trxn_entry',])
           
 
      #trnxndate = dftrxn['TXNDATE'][0]

      subtotal = total_price + gstaddsum


      df3['delivery_status'] = ["❌ Not Delivered " if (x== 0 ) else "✅ Delivered" for x in df3.process_status]



#creating final  data structure
        
      finalds = df3.to_numpy().tolist()      

      df3 = df3.to_html(classes=["table-bordered",])
      context = {'df3': df3,
             'recentcartcount':recentcartcount,
             'finalds':finalds,
             'total_price':total_price,
             'discount':discount,
             'gstaddsum':gstaddsum,
             'subtotal' :subtotal,
             }

      return render(request, 'order_category_page.html',context)


def orderpage(request,orderid,productid):
      user = User();
             
      if user.is_authenticated:
#CART CHECK FILL VALUE DYNAMICALLY
            cartfiltertable=Cart.objects.all().values_list('quantity').filter(Q(username=request.user.username) )
            df = pd.DataFrame(cartfiltertable, columns=['quantity',])


            df=df.sum(axis = 0, skipna = True) 
      
            recentcartcount =int(df.quantity)
    
      

#############################################
      Order_sucked=Order.objects.all().values_list('title','discount_price','orderid','Address','landmark','locality','city','state','country','payment_mode','zipcode','mobileno','Product_id','total_price','size','quantity','gst_added_price','process_status','tracking_status').filter(Q(username=request.user.username) & Q(orderid = orderid) & Q(Product_id = productid))
      df0 = pd.DataFrame(Order_sucked, columns=['title','discount_price','orderid','Address','landmark','locality','city','state','country','payment_mode','zipcode','mobileno','Product_id','total_price','size','quantity','gst_added_price','process_status','tracking_status'])

      dfcap  =df0

#EXTRACTING MULTIPLE PRODUCT IMAGES PATH
                
      Image_Path_filtertable=ImgPath.objects.all().values_list('path1','Product_id')
      df1 = pd.DataFrame(Image_Path_filtertable, columns=['path1','Product_id'])



#EXTRACTING MULTIPLE PRODUCT ATTRIBUTES
                
      Product_filtertable=Product.objects.all().values_list('Product_id','category',)
      df2= pd.DataFrame(Product_filtertable, columns=['Product_id','category',])



      df1 = reduce(lambda x,y: pd.merge(x,y, on=['Product_id',], how='outer'), [df1, df0])

      df2 = reduce(lambda x,y: pd.merge(x,y, on=['Product_id',], how='outer'), [df2, df1])

      df3 =df2

      df3 = df3.drop_duplicates()    #dropping duplicate rows

      df3 = df3.dropna()         #dropping all null values


     # orderid = int(df3['orderid'][0])

      df3['total_price'] = df3['total_price'].astype(np.int64)
      df3['size'] = df3['size'].astype(np.int64)
      df3['discount_price'] = df3['discount_price'].astype(np.int64)
      df3['quantity'] = df3['quantity'].astype(np.int64)



##############################  VARIOUS VALUES CALCULATIONS
     # orderid = df3['orderid'][0]

      
      total_price =int(df3['total_price'].sum())


      discount = 0

      gstaddsum =(total_price/100)*18 
                
    
      TransactionDetails_qs=TransactionDetails.objects.all().values_list('trxn_entry',)
      dftrxn = pd.DataFrame(TransactionDetails_qs, columns=['trxn_entry',])
           
 
      #trnxndate = dftrxn['TXNDATE'][0]
############## TRACKING ACTIVE/DEACTIVATE STATUS CODE
      subtotal = total_price + gstaddsum

      df3 = df3.reset_index()

      df3 = df3.drop(['index'], axis=1)
      
      df3['active1']  = ''
      df3['active2']  = ''
      df3['active3']  = ''
      df3['active4']  = ''



      for x in range(len(df3)):
            if df3.loc[x,'tracking_status'] == 'ordered':        #accesing tracking_status rall rows
                  df3.loc[x,'active1']= 'active'

      for x in range(len(df3)):
            if df3.loc[x,'tracking_status'] == 'packed':
                  df3.loc[x,'active1']= 'active'
                  df3.loc[x,'active2']= 'active'
      for x in range(len(df3)):
            if df3.loc[x,'tracking_status'] == 'shipped':
                  df3.loc[x,'active1']= 'active'
                  df3.loc[x,'active2']= 'active'
                  df3.loc[x,'active3']= 'active'

               
      for x in range(len(df3)):
            if df3.loc[x,'tracking_status'] == 'delivered':
                  df3.loc[x,'active1']= 'active'
                  df3.loc[x,'active2']= 'active'
                  df3.loc[x,'active3']= 'active'
                  df3.loc[x,'active4']= 'active'


        
#creating final  data structure
        
      finalds = df3.to_numpy().tolist()      

      df3 = df3.to_html(classes=["table-bordered",])
      context = {'df3': df3,
             'recentcartcount':recentcartcount,
             'finalds':finalds,
             'total_price':total_price,
             'discount':discount,
             'gstaddsum':gstaddsum,
             'subtotal' :subtotal,
             'orderid':orderid,
             'dfcap':dfcap,
             }
      return render(request, 'orderpage.html',context)



import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
def receipt_creator(request):
    """Generate pdf."""
    # Model data
    Order_sucked=Order.objects.all().values_list('title','discount_price','orderid','Address','landmark','locality','city','state','country','payment_mode','zipcode','mobileno','Product_id','total_price','size','quantity','gst_added_price','process_status','tracking_status').filter(Q(username=request.user.username) )
    df = pd.DataFrame(Order_sucked, columns=['title','discount_price','orderid','Address','landmark','locality','city','state','country','payment_mode','zipcode','mobileno','Product_id','total_price','size','quantity','gst_added_price','process_status','tracking_status'])

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    p.setFont('Helvetica', 12)
    p.line(17, 797, 580, 797) #FROM TOP 1ST LINE
    p.drawString(250, 800, "TAX INVOICE")
    p.drawString(60, 720, "COMPANY NAME:- "+ 'val1')
    p.drawString(60, 690, "EMAIL-ID:- "+ 'val2')
    p.drawString(60, 660, "ADDRESS:- "+ 'val3')
    p.drawString(450, 720, "DATE :- "+ 'val4')
    p.line(450, 710, 560, 710)
    p.line(17, 640, 580, 640)#FROM TOP 2ST LINE
    p.line(17, 797, 17, 50)#LEFT LINE
    p.line(400, 640, 400, 50)# MIDDLE LINE
    p.line(580, 797, 580, 50)# RIGHT LINE
    p.drawString(475, 615, 'TOTAL AMOUNT')
    p.drawString(100, 615, 'PRODUCT')
    p.line(17, 600, 580, 600)#FROM TOP 3rd LINE
    p.drawString(60, 550, 'val5')
    p.drawString(500, 550, 'val6')
   # TOTAL = int(amountpdf) * ((int(staxpdf)) / 100)
    p.drawString(60, 500, "SERVICE TAX (" +'val8'+"%)")
    p.drawString(500, 500, 'val9')
    p.line(17, 100, 580, 100)#FROM TOP 4th LINE
    p.drawString(60, 80, " TOTAL AMOUNT")
    p.drawString(500, 80, 'val10')
    p.line(17, 50, 580, 50)#FROM TOP LAST LINE
    p.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='invoice.pdf')



def saved_adresses(request):
  return render(request, 'savedaddress.html')

  