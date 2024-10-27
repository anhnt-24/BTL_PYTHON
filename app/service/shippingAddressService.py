from .userservice import getUser
from ..models import ShippingAddress
def getDefaultAddress(request):
    try:
        user=getUser(request)
        default=ShippingAddress.objects.filter(user=user,default=True)[0]
    except:
        return None
    return default

def getNotDefaultAddress(request):
    try:
        user=getUser(request)
        notDefault=ShippingAddress.objects.filter(user=user,default=False)
    except:
        return None
    return notDefault

def getAllAddress(request):
    l=[]
    default=getDefaultAddress(request)
    notDefault=getNotDefaultAddress(request)
    if default:
        l.append(default)
    if notDefault:
        l+=notDefault
    return l

def getAddressById(id):
    return ShippingAddress.objects.get(id=id)


def deleteAddressById(id):
    address=ShippingAddress.objects.get(pk=id)
    address.delete()

def mappingAddressForm(request,address):
    address.receiver=request.POST.get('receiver')    
    address.phone=request.POST.get('phone')
    address.commune=request.POST.get('commune')
    address.district=request.POST.get('district')
    address.province=request.POST.get('province')
    address.detail=request.POST.get('detail')
    address.id_province = request.POST.get('id_province')
    address.id_commune = request.POST.get('id_commune')
    address.id_district = request.POST.get('id_district')
    return address

def updateAddressById(request,id):
    if(request.method=='POST'):
        address=ShippingAddress.objects.get(pk=id)
        address=mappingAddressForm(request,address)
        address.save()

def createNewAddress(request):
    if(request.method=='POST'):
        user=getUser(request)
        address=ShippingAddress(user=user)
        address=mappingAddressForm(request,address)
        if not ShippingAddress.objects.filter(user=user).first():
            address.default=True
        address.save()

def setDefaultAddress(request,id):
    addressDefault=getDefaultAddress(request)
    addressDefault.default=False
    addressDefault.save()

    addressNotDefault=ShippingAddress.objects.get(pk=id)
    addressNotDefault.default=True
    addressNotDefault.save()
    
