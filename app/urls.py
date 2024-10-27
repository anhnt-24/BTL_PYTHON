from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.urls import re_path
from django.views.static import serve

urlpatterns = [
    path('login',loginView,name='login'),
    path('register',register,name='register'),
    


    path('',home,name='home'),
    path('productdetail/<int:id>',productdetail,name='productdetail'),

    path('my-cart',cart,name='cart'),
    path('my-cart/add',addCart,name='addCart'),
    path('my-cart/delete/multi',delMultiCartItem,name='delMultiCartItem'),
    path('my-cart/delete/<int:id>',delCartItem,name="deleteCartItem"),
    path('my-cart/quantity/<int:id>/<int:quantity>',cartItemQuantity,name="setCartItemQuantity"),

    path('payment',payment,name='payment'),
    path('payment/address',paymentAddress,name='paymentAddress'),
    path('payment/process/mono',processPaymentMono,name="proccessPaymentMono"),
    path('payment/process/multi',processPaymentMulti,name='proccessPaymentMulti'),
    path('payment/apply/discount/code',paymentDiscount,name='paymentDiscount'),
    path('payment/remove/discount/code',paymentDiscountRemove,name='paymentDiscountRemove'),

    path('my-order',order,name='my-order'),
    path('my-order/address/<int:order_id>',orderAddress,name='orderAddress'),
    path('my-order/add',addOrder,name='addOrder'),
    path('my-order/delete/<int:id>',delOrderItem,name='delOrderItem'),
    path('my-order/success/<int:id>',orderStatusToSuccess,name='orderSuccess'),

    path('my-info',user,name='my-info'),
   
    path('logout',logoutView,name='logout'),
    path('contact',contact,name='contact'),
    path('about-us',about_us,name='about-us'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

    path('my-info/update',userUpdate,name='userUpdate'),

    path('my-address',userAddress,name='address'),
    path('my-address/delete/<int:id>/',deleteAddress,name='deleteAddress'),
    path('my-address/update/<int:id>/',updateAddress,name='updateAddress'),
    path('my-address/create/',createAddress,name='createAddress'),
    path('my-address/set-default-address/<int:id>',setDefaultAddr,name='setDefaultAddr'),

    path('getall',getAll),

    path('authenticate/forget/password',forgetPassword,name="forgetPassword"),
    path('authenticate/forget/username',forgetUsername,name="forgetUsername"),
    path('authenticate/confirmation',confirmationNewAuthenticate,name="confirmationNewAuthenticate"),
    path('authenticate/change/password/<str:token>',changePassword,name="changePassword"),
    path('authenticate/change/email/<str:token>',changeEmail,name="changeEmail"),
    path('authenticate/change/phone/<str:token>',changePhone,name="changephone"),
    path('authenticate/send/change/password',sendChangePassword,name="sendChangePassword"),
    path('authenticate/send/change/email',sendChangeEmail,name="sendChangeEmail"),
    path('authenticate/send/change/phone',sendChangePhone,name="sendChangePhone"),
    
    path('lookupOrder',lookupOrder,name="lookupOrder"),
    path('lookupOrder/result',lookupOrderResult,name="lookupOrderResult"),

    path('search/product',searchProduct,name="searchProduct"),

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)