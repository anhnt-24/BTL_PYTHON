from django.shortcuts import render, redirect,HttpResponse
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .handlefunc import *
from .service.service import *
from django.contrib import messages
import secrets
# Create your views here.
from allauth.socialaccount.providers.facebook.views import oauth2_login
def direct_facebook_login(request):
    return oauth2_login(request)

def register(request):
    error_message = None 
    if request.method == 'POST':
        username = request.POST.get("username")
        if User.objects.filter(username=username).exists():
            error_message='Tên tài khoản đã tồn tại, vui lòng nhập lại!'
            return render(request, 'register.html',{'error':error_message})
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        email = request.POST.get("email")
        if Customer.objects.filter(email=email).exists():
            error_message='Tên Email đã tồn tại, vui lòng chọn Email khác!'
            return render(request, 'register.html',{'error':error_message})
        phone = request.POST.get("phone")
        if Customer.objects.filter(phone=phone).exists():
            error_message='Số điện thoại đã tồn tại, vui lòng chọn số khác!'
            return render(request, 'register.html',{'error':error_message})
        backend="django.contrib.auth.backends.ModelBackend"
        user = User.objects.create_user(username=username, password=password)
        user.backend=backend
        user.save()
        Customer.objects.create(user=user,email=email,phone=phone)
        login(request, user)
        return redirect('home')
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'register.html',{'error':error_message})

@never_cache
def loginView(request):
    if request.user.is_authenticated:
        return redirect('home')
    error_message = None 
    if request.method == 'POST':
        username = request.POST.get("username")  
        password = request.POST.get("password")  
        user = authenticate(request, username=username, password=password)  
        if user is not None:  
            login(request, user)  
            next_url = request.POST.get('next') or request.GET.get('next') or 'home'  
            return redirect(next_url) 
        else:
            error_message = "Tài khoản hoặc mật khẩu sai, vui lòng thử lại!" 
            return render(request, 'login.html', {'error': error_message})
    return render(request, 'login.html')

def logoutView(request):
    if(request.method=='POST'):
        logout(request)
        return redirect('login')
    return redirect('home')

@login_required
def home(request):
    if request.method=="POST":
        messages.success(request,"Yêu cầu của bạn đã được lưu lại")
        return redirect("home")
    slider=getAllSlider()
    context={
        'slider':slider,
        'list':getAllGeneralCategoryDetail()
    }

    return render(request,'home.html',context)

@login_required
def cart(request):
    ok=False
    if(request.session.get('ok')):
        ok=True
        del request.session['ok']
    
    context={
        'ok':ok,
        'cart':getAllCartItemByUserDetail(request)
    }
    return render(request,'cart.html',context)

@login_required
def addCart(request):
    if(request.method=="POST"):
        addCartItem(request) 
        request.session['ok']=True
        return redirect('cart')
    return redirect('cart')

@login_required
def delMultiCartItem(request):
    deleteMultiCartItem(request)
    return redirect('cart')

@login_required
def delCartItem(request,id):
    deleteCartItem(id)
    return redirect('/my-cart')

@login_required
def cartItemQuantity(request,id,quantity):
    setCartItemQuantity(id,quantity)
    return redirect('cart')

@login_required
def order(request):
    return render(request,'order.html',context=getAllOrder(request))

@login_required
def addOrder(request):
    if request.method=="POST":
        createOrder(request)
    return redirect('my-order')

@login_required
def delOrderItem(request,id):
    if request.method=="POST":
        deleteOrderItem(request,id)
    return redirect('my-order')

@login_required
def orderStatusToSuccess(request,id):
    if request.method=="POST":
        updateOrderStatus(request,id)
    return redirect('my-order')

@login_required
def orderAddress(request,order_id):
    if request.method=="POST":
        changeOrderItemAddress(request,order_id)
    return redirect('my-order')

@login_required
def paymentAddress(request):
    if request.method=="POST":
        resovlePaymentAddress(request)
        return redirect("payment")
    return redirect("home")

@login_required
def paymentDiscount(request):
    if request.method=="POST":
        resolveDiscount(request)
        if(request.session.get("discount")!=None):
            messages.success(request,"Thành công")
        else:
            messages.info(request,"Mã giảm giá không hợp lệ")
    return redirect("payment")

@login_required
def paymentDiscountRemove(request):
    resovelDiscountRemove(request)
    return redirect("payment")

@login_required
def processPaymentMono(request):
    if request.method=="POST":
        resolvePaymentMono(request)
        return redirect('payment')
    return redirect("home")

@login_required
def processPaymentMulti(request):
    if request.method=="POST":
        resolvePaymentMulti(request)
        return redirect("payment")
    return redirect("home")

@login_required
def payment(request):
    if(request.session.get("total")==None):
        messages.info(request,"Bạn chưa có đơn thanh toán nào.")
        return redirect("home")
    
    context={
        'payment':resolvePayment(request),
    }
    return render(request,'payment.html',context)

@login_required
def productdetail(request,id):

    context={
        "product":getProductByIDDetail(id)
    }
    return render(request,'productdetail.html',context)

@login_required
def user(request):
    
    try:
        customer=getCustomer(request)
        birth=dateHdl(customer.birth)
        name=nameHdl(customer.name)
        
        email= emailHdl(customer.email)  
        phone=phoneHdl(customer.phone)
        img=customer.img
        gender=customer.gender
        ok=False
        if(request.session.get("updateUser")):
            ok=True
            del request.session["updateUser"]
        context={'customer':customer,
                 'birth':birth,
                 'name' :name,
                  'phone':phone,
                  'email':email,  
                  'img':img,
                  'gender':gender,
                  "updateUser":ok
        }
        return render(request,'user.html',context)
    except Exception:
        pass
    return render(request,'user.html')
    
@login_required
def userUpdate(request):

    if request.method=='POST':
        email=request.POST.get('email') or ""
        phone=request.POST.get('phone') or ""
        customer=getCustomer(request)
        if email !="":
            if(getUserByEmail(email)[0]!=None):
                messages.info(request,"Email đã tồn tại.")
                return redirect("my-info")
            else:
                customer.email=email
        if phone !="":    
            if(phone !="" and getUserByPhone(phone)[0]!=None):
                messages.info(request,"Số điện thoại đã tồn tại.")
                return redirect("my-info")
            else:
                customer.phone=phone

        customer.name=request.POST.get('name').strip()
        customer.gender=request.POST.get('gender') or customer.gender
        customer.birth=strToDate(request.POST.get('dob'))
        customer.img=request.FILES.get("file") or customer.img
            
        customer.save()
        request.session["updateUser"]=True
    return redirect('/my-info')

@login_required
def contact(request):
    return HttpResponse('chaoem nha')

@login_required
def about_us(request):
    return HttpResponse('Chao em nha!')

@login_required
def view404(request,exception):
    return render(request,'404view.html',{})

@login_required
def userAddress(request):

    message=None
    if request.session.get('address'):
        message=request.session.get('address')
        del request.session['address']
    
    context={
        'listAddress':getAllAddress(request),
        'message':message
    }
    print(context)
    return render(request,'shippingAddress.html',context)

@login_required
def deleteAddress(request,id):
    deleteAddressById(id)
    return redirect('/my-address')

@login_required
def updateAddress(request,id):
    request.session['address']='Cập nhật thành công'
    updateAddressById(request,id)
    return redirect('/my-address')

@login_required
def createAddress(request):
    request.session['address']='Tạo mới thành công'
    createNewAddress(request)
    return redirect('/my-address')
@login_required
def setDefaultAddr(request,id):
    setDefaultAddress(request,id)
    return redirect('/my-address')

def getAll(request):
    x=getAllGeneralCategoryDetail()
    return HttpResponse('ok')

def forgetPassword(request):
    if(request.method=="POST"):
        [user,customer]=getUserByUsername(request)
        if(user==None):
            messages.error(request, 'Tên đăng nhập không tồn tại')
            return redirect("forgetPassword")
        if(customer.email== None):
            messages.error(request, 'Tài khoản của bạn chưa đăng kí Email, hết cứu!!!')
            return redirect("forgetPassword")
        
        token = secrets.token_hex(16) 
        request.session['token'] = token
        email=emailHdl(customer.email)
        otp=generateOTP()
        request.session["otp"]=otp
        request.session["user"]=user.id
        request.session.set_expiry(300)
        host=request.get_host()
        link='/authenticate/change/password/'
        default_link=f"{link}{token}"
        link=f"http://{host}{link}{token}"
        linkSendAgain='/authenticate/forget/password'
        data=[
            'username',request.POST.get("username")
        ]
        request.session["linkSendAgain"]=linkSendAgain
        request.session["data"]=data
        sendEmail("Quên mật khẩu",f"""
            <p>Xin chào,</p>
            <br>
            <p>Bạn đã yêu cầu mã xác minh cho tài khoản của mình.</p>
            <p>Mã xác minh của bạn là: <strong>{otp}</strong></p>
            <p>Vui lòng không chia sẻ mã này cho bất kì ai.</p>
            <br>
            <p>Hoặc bạn có thể nhấp vào đường dẫn sau đây để đi đến trang thay đổi:</p>
            <p><a style='color: blue; text-decoration: underline;' href='{link}'>{link}</a><p>
            <br>
            <h2>FROM SOPI WITH LOVE <span style="color:red;">&#10084;<span></h2>""",customer.email)
        messages.success(request, f'Chúng tôi đã gửi OTP đến {email} , vui lòng kiểm tra.')
        request.session["next"]=f"{default_link}"
        return redirect("confirmationNewAuthenticate")
    listInput=[["username","Tên đăng nhập:","Tên đăng nhập"]]
    context={
        "title":"Quên mật khẩu",
        "listInput":listInput,
        "next":"/authenticate/forget/password"
    }
    return render(request,"authenticate.html",context)

def forgetUsername(request):
    if(request.method=="POST"):
        [user,customer]=getUserByEmail(request)
        if(user==None):
            messages.error(request, 'Tài khoản Email này chưa được đăng kí.')
            return redirect("forgetUsername")
        messages.success(request, f'Chúng tôi đã gửi tên tài khoản và mã xác minh đến {customer.email} , vui lòng kiểm tra.')
        token = secrets.token_hex(16) 
        request.session['token'] = token
        otp=generateOTP()
        request.session["otp"]=otp
        request.session["user"]=user.id
        request.session.set_expiry(300)
        host=request.get_host()
        link='/authenticate/change/password/'
        default_link=f"{link}{token}"
        link=f"http://{host}{link}{token}"
        sendEmail("Quên tài khoản",f"""
                <p>Xin chào,</p>
            <br>
            <p>Bạn đã yêu cầu khôi phục lại tài khoản của mình:</p>
            <span>Tài khoản:</span> <strong>{user.username}</strong><br>
            <p>Mã xác minh của bạn là: <strong>{otp}</strong></p>
            <p>Hãy dùng mã xác minh này để đặt lại mật khẩu mới.</p>
            <p>Vui lòng không chia sẻ mã này cho bất kì ai.</p>
            <br>
            <p>Hoặc bạn có thể nhấp vào đường dẫn sau đây để đi đến trang thay đổi:</p>
            <p>
                <a href="{link}">{link}</a>
            </p>
            <br>
            <h2>FROM SOPI WITH LOVE <span style="color: red;">&#10084;</span></h2>
        """,customer.email)

        linkSendAgain='/authenticate/forget/username'
        data=[
            'email',request.POST.get("email")
        ]
        request.session["linkSendAgain"]=linkSendAgain
        request.session["data"]=data
        request.session["next"]=f"{default_link}"
        return redirect("confirmationNewAuthenticate")
    listInput=[["email","Vui lòng nhập Email đã đăng kí:","Email"]]
    context={
        "title":"Quên tài khoản",
        "listInput":listInput,
        "next":"/authenticate/forget/username"
    }
    return render(request,"authenticate.html",context)
def confirmationNewAuthenticate(request):
    if(request.method=="POST"):
        if(request.POST.get("otp")!=request.session.get("otp")):
            messages.error(request, 'Mã xác minh không chính xác.')
            return redirect("confirmationNewAuthenticate")
        messages.success(request, 'Xác thực thành công.')
        next=request.session.get("next")
        return redirect(f"{next}")
    
    listInput=[["otp","Vui lòng nhập mã xác minh:","Mã xác minh"]]
    context={
        "title":"Xác minh OTP",
        "listInput":listInput,
        "next":'/authenticate/confirmation',
        "data":request.session.get("data"),
        "linkSendAgain":request.session.get("linkSendAgain")

    }
    return render(request,"authenticate.html",context)
def changePassword(request,token):
    if(token!=request.session.get("token")): return redirect("home")
    if(request.method=="POST"):
        password=request.POST.get("password")
        if(request.session.get("user")==None):
            user=getUser(request)
        else:
            user=getUserById(request.session.get("user"))
        user.set_password(password)
        user.save()
        messages.success(request, 'Đổi mật khẩu thành công')
        del request.session['token']
        return redirect("login")
    listInput=[["password","Mật khẩu mới:","Mật khẩu"],
                ["confirmpassword","Xác nhận mật khẩu:","Xác nhận mật khẩu"]]
    context={
        "title":"Đổi mật khẩu",
        "listInput":listInput,
        "next":f"/authenticate/change/password/{token}"
    }
    return render(request,"authenticate.html",context)

def sendEmailChange(request,message,link):
    otp=generateOTP()
    token = secrets.token_hex(16) 
    request.session['token'] = token
    request.session["otp"]=otp
    request.session.set_expiry(300)
    email=getCustomer(request).email
    if(email==None):
        messages.info(request, "Tài khoản của bạn chưa liên kết với bất kì Email nào.")
        return redirect("home")
    host=request.get_host()
    default_link=f"{link}{token}"
    link=f"http://{host}{link}{token}"
    request.session["next"]=default_link
    messages.success(request, f'Chúng tôi đã gửi OTP đến {emailHdl(email)} , vui lòng kiểm tra.')
    sendEmail(message,f"""
            <p>Xin chào,</p>
            <br>
            <p>Bạn đã yêu cầu mã xác minh cho tài khoản của mình.</p>
            <p>Mã xác minh của bạn là: <strong>{otp}</strong></p>
            <p>Vui lòng không chia sẻ mã này cho bất kì ai.</p>
            <br>
            <p>Hoặc bạn có thể nhấp vào đường dẫn sau đây để đi đến trang thay đổi:</p>
            <p><a style='color: blue; text-decoration: underline;' href='{link}'>{link}</a><p>
            <br>
            <h2>FROM SOPI WITH LOVE <span style="color:red;">&#10084;<span></h2>""",email)
    return redirect("confirmationNewAuthenticate")

@login_required
def sendChangePassword(request):
    linkSendAgain='authenticate/send/change/password'
    request.session["linkSendAgain"]=linkSendAgain
    return sendEmailChange(request,"Đổi mật khẩu","/authenticate/change/password/")

@login_required
def sendChangePhone(request):
    linkSendAgain='authenticate/send/change/phone'
    request.session["linkSendAgain"]=linkSendAgain
    return sendEmailChange(request,"Thay đổi số điện thoại","/authenticate/change/phone/")

@login_required
def sendChangeEmail(request):
    linkSendAgain='authenticate/send/change/email'
    request.session["linkSendAgain"]=linkSendAgain
    return sendEmailChange(request,"Thay đổi Email","/authenticate/change/email/")

@login_required
def changeEmail(request,token):
    if(token!=request.session.get("token")): return redirect("home")
    if(request.method=="POST"):
        if(getUserByEmail(request)[0] != None):
             messages.error(request, 'Tài khoản Email đã tồn tại.')
             return redirect("/authenticate/change/email")
        customer=getCustomer(request)
        email=request.POST.get("email")
        customer.email=email
        customer.save()
        messages.success(request, 'Thay đổi Email thành công!')
        del request.session['token']
        return redirect("my-info")
    listInput=[["email","Email mới:","Email"]]
    context={
        "title":"Thay đổi Email",
        "listInput":listInput,
        "next":f"/authenticate/change/email/{token}"
    }
    return render(request,"authenticate.html",context)


@login_required
def changePhone(request,token):
    if(token!=request.session.get("token")): return redirect("home")
    if(request.method=="POST"):
        if(getUserByPhone(request)[0] != None):
             messages.error(request, 'Số điện thoại đã tồn tại.')
             return redirect("/authenticate/change/phone")
        customer.phone=request.POST.get("phone")
        customer=getCustomer(request)
        customer.save()
        messages.success(request, 'Thay đổi số điện thoại thành công!')
        del request.session['token']
        return redirect("my-info")
    listInput=[["phone","Số điện thoại mới:","Số điện thoại"]]
    context={
        "title":"Thay đổi số điện thoại",
        "listInput":listInput,
        "next":f"/authenticate/change/phone/{token}"
    }
    return render(request,"authenticate.html",context)
    
def lookupOrder(request):
    return render(request,"lookup.html")

def lookupOrderResult(request):
    if(request.method=="POST"):
        order=getOrderByCode(request)
        code=request.POST.get("code")
        print(code)
        if(order==None):
            messages.error(request,"Mã đơn hàng không tồn tại.")
            return redirect("lookupOrder")
        messages.success(request,f"Kết quả tra cứu cho mã {code}")
        return render(request,"lookup.html",context=order)
    return redirect("lookupOrder")

@login_required
def searchProduct(request):
    product=searchPro(request)
    return render(request,"search.html",context=product) 