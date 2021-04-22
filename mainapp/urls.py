from django.urls import path,include,re_path

from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('category_main/', views.category_main, name="category_main"),
    path('category_filter/', views.category_filter, name='category_filter'),
    path('category_filter_delete/<str:filterval>/', views.category_filter_delete, name='category_filter_delete'),
    path('search_term/', views.search_term, name='search_term'),
    path('coupon_apply', views.coupon_apply, name='coupon_apply'),
    path("handlerequest/", views.handlerequest, name="HandleRequest"),
    path("charge_val_get/", views.charge_val_get, name="charge_val_get"),




    path('Contact/', views.Contact, name="Contact"),
    path('Contact/ContactFormRecieved', views.ContactFormRecieved, name="ContactFormRecieved"),

    path('productinfo/<int:itemid>/', views.productinfo, name="productinfo"),


    path('signup/', views.signup, name='signup'),
    path('view_login/', views.view_login, name='view_login'),
    path('view_logout/', views.view_logout, name='view_logout'),
    path('cartpage/', views.cartpage, name='cartpage'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('delete_from_cart/<int:itemid>/', views.delete_from_cart, name='delete_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/place_order', views.place_order, name='place_order'),

    
    path('calculate/', views.calculate, name='calculate'),









   # path('accounts/', include('django.contrib.auth.urls')),
   
   # path('addtocart/<int:itemid>/', views.addtocart, name='addtocart'),
   # path('deletefromcart/<int:itemid>/', views.deletefromcart, name='deletefromcart'),





]



