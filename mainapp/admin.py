from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from .models import *



class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('name', 'email','Subject','text_message','created_Entry_date')
admin.site.register(ContactForm, ContactFormAdmin)






class ProductAdmin(ImportExportModelAdmin):
    list_display = ( 'Product_id','title','brand','color','price','size','discount_price','avail_status','category',)
    list_filter = ('brand','avail_status','category','Product_id', )

admin.site.register(Product, ProductAdmin)




class CartAdmin(admin.ModelAdmin):
    list_display = ('username','Product_id','title','size','quantity','discount_price','total_price','price', 'date_added')
    list_filter = ('username','Product_id','date_added', )

admin.site.register(Cart, CartAdmin)


class cartpage_info_admin(admin.ModelAdmin):
    list_display = ('username','orderid','chargevalue')

admin.site.register(cartpage_info, cartpage_info_admin)




class ImgPathAdmin(ImportExportModelAdmin):
    list_display = ( 'capture_value','Product_id','path1','path2','path3','path4','thumbpath1','thumbpath2','thumbpath3','thumbpath4','related_product_path_1','related_product_path_2','related_product_path_3','related_product_path_4','related_product_path_5',)
admin.site.register(ImgPath, ImgPathAdmin)






class order2Admin(admin.ModelAdmin):
    list_display = ('username','Address','landmark','locality','city','state','country','payment_mode','zipcode', 'mobileno','alt_mobileno','date_added')
    list_filter = ('username','date_added', )

admin.site.register(order2, order2Admin)



class OrderAdmin(admin.ModelAdmin):
    list_display = ('username','orderid','process_status','Address','landmark','locality','city','state','country','tracking_status','gst_added_price','payment_mode','zipcode','mobileno','alt_mobileno','Product_id','title','discount_price','total_price','size','quantity','date_added')
    list_filter = ('username','process_status')

admin.site.register(Order, OrderAdmin)




class filterinfoAdmin(admin.ModelAdmin):
    list_display = ('username','category_call','price_call','color_call','brand_call','size_call','date_added')
    list_filter = ('username','category_call','price_call','color_call','brand_call','size_call','date_added')

admin.site.register(filterinfo, filterinfoAdmin)




class searchinfoAdmin(ImportExportModelAdmin):
    list_display = ('std_search_term',)

admin.site.register(searchinfo, searchinfoAdmin)




class searchinfo_by_user_admin(ImportExportModelAdmin):
    list_display = ('username','search_req',)
    list_filter = ('username','search_req',)

admin.site.register(searchinfo_by_user, searchinfo_by_user_admin)





class TransactionDetails_admin(ImportExportModelAdmin):
    list_display = ('trxn_entry',)

admin.site.register(TransactionDetails, TransactionDetails_admin)

