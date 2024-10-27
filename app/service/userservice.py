from ..models import Customer
from django.contrib.auth.models import User
from django.core.mail import send_mail
import pyotp
from django.conf import settings
def getUser(request):
    user = User.objects.get(pk=request.user.id) 
    return user
def getUserById(id):
    return User.objects.get(pk=id)

def getCustomer(request):
    user = getUser(request)
    customer=None
    try:
        customer=Customer.objects.get(user=user)
        return customer
    except:
        customer= Customer(user=user)
        customer.save()
        return customer

def getUserByUsername(request):
    try:
        username=request.POST.get("username")
        user=User.objects.get(username=username)
        customer=Customer.objects.get(user=user)
        return [user,customer]
    except:
        return [None,None]

def getUserByPhone(request):
    try:
        phone=request.POST.get("phone")
        customer=Customer.objects.get(phone=phone)
        return [customer.user,customer]
    except:
        return [None,None]


def getUserByEmail(request):
    try:
        email=request.POST.get("email")
        customer=Customer.objects.get(email=email)
        return [customer.user,customer]
    except:
        return [None,None]

def generateOTP():
    secret_key = pyotp.random_base32()  
    totp = pyotp.TOTP(secret_key)
    otp_code = totp.now() 
    return otp_code

def sendEmail(subject,message,toEmail):
    send_mail(
    subject,
    '',
    settings.EMAIL_HOST_USER,
    [toEmail],
    fail_silently=False,
    html_message=message
)