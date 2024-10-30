from ..models import CartItem
from .userservice import getUser
from .productService import*

def getAllCartItemByUser(request):
    return CartItem.objects.filter(user=getUser(request))
def getCartItemByID(id):
    return CartItem.objects.get(id=id)

def addCartItem(request):

    quantity=int(request.POST.get("quantity"))
    price=int(request.POST.get("price"))
    color_size=getColor_SizeByMTM(request.POST.get("size"),request.POST.get("color"))
    total=price*quantity
    cartItem=CartItem.objects.filter(user=getUser(request),color_size=color_size)
    if(cartItem):
        cartItem=cartItem[0]
        cartItem.quantity+=quantity
        cartItem.total+=total
    else:
        cartItem=CartItem(user=getUser(request))
        cartItem.color_size=color_size
        cartItem.price=price
        cartItem.quantity=quantity
        cartItem.total=total

    cartItem.save()
    
def getAllCartItemByUserDetail(request):
    cartItem=getAllCartItemByUser(request)
    l=[]
    for item in cartItem:
        color_size=item.color_size
        color=color_size.color
        size=color_size.size
        product=size.product
        l.append({
            "color":color,
            "size":size,
            "product":product,
            "total":item.total,
            "quantity":item.quantity,
            "id":item.id
        })
    return l

def deleteCartItem(id):
    CartItem.objects.get(id=id).delete()

def setCartItemQuantity(id,quantity):
    cartItem=CartItem.objects.get(id=id)
    cartItem.quantity=quantity
    cartItem.total=quantity*cartItem.price
    cartItem.save()

def deleteMultiCartItem(request):
    for id in request.POST.getlist("cartItem[]"):
        deleteCartItem(id)

def deleteMultiCartItemByList(list):
    for id in list:
        deleteCartItem(id)