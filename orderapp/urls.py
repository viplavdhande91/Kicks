from django.urls import path,include,re_path

from . import views
urlpatterns = [
    path('order_category_page/', views.order_category_page, name="order_category_page"),
    re_path(r'^orderpage//?(?P<orderid>[0-9]+)?//?(?P<productid>[0-9]+)?/$', views.orderpage ,name = 'orderpage'),
    path('receipt_creator/', views.receipt_creator, name="receipt_creator"),
    path('saved_adresses/', views.saved_adresses, name="saved_adresses"),




  






]



