from .color_sizeService import getColor_SizeByMTM,getColor_SizeByID
from .shippingAddressService import getAllAddress,getAddressById,getDefaultAddress
from .cartService import getCartItemByID
from .messageService import *
from .discountService import getDiscountByCode

def resolvePaymentMono(request):
    price=int(request.POST.get("price"))
    quantity=int(request.POST.get("quantity"))
    color_size_list=[getColor_SizeByMTM(request.POST.get("color"),request.POST.get("size")).id]
    item_total=price*quantity
    total=item_total
    request.session["deliveryFee"]=20000
    request.session['color_size']=color_size_list
    request.session['quantity']=[quantity]
    request.session['item_total']=[item_total]
    request.session['total']=total
    request.session['cartItem[]']=[]

def resolvePaymentMulti(request):
    quantity=request.POST.getlist("quantity[]")
    cartItem=request.POST.getlist("cartItem[]")
    total=request.POST.get("total")
    color_size_list=[]
    item_total=[]
    
    for item in cartItem:
        color_size_list.append(getCartItemByID(item).color_size.id)
        item_total.append(getCartItemByID(item).total)

    request.session["deliveryFee"]=20000
    request.session['color_size']=color_size_list
    request.session['quantity']=quantity
    request.session['total']=total
    request.session['item_total']=item_total
    request.session['cartItem[]']=cartItem
    
def resolvePayment(request):

    deliveryFee=request.session.get("deliveryFee")
    quantity=request.session.get("quantity")
    color_size_list=request.session.get("color_size")
    total_item=request.session.get('item_total')
    total=int(request.session.get("total"))
    pretotal=total
    discount=request.session.get("discount") or 0
    code=request.session.get("code") or ""
    avg=(-discount+deliveryFee)//len(total_item)
    l=[]
    for i in total_item:
        l.append(i+avg)
    total_item=l
    total=total-discount+deliveryFee
    if(request.session.get('payment_address')):
        id_addressDefault=request.session.get('payment_address')
        addressDefault=getAddressById(id_addressDefault) 
    else:
        addressDefault=getDefaultAddress(request)
    message=None
    if(request.session.get("payment_address_update")):
        message="Thay đổi địa chỉ thành công."
        del request.session['payment_address_update']
    l=[]
    for i in range(len(color_size_list)):
        color_size=getColor_SizeByID(color_size_list[i])
        product=color_size.size.product

        l.append({
            "size":color_size.size.size,
            "color":color_size.color.color,
            "img":color_size.color.img,
            "quantity":quantity[i],
            "total_item":total_item[i],
            "product":product,
            "color_size":color_size
        })
    return{
        "list":l,
        "total":total,
        "address":getAllAddress(request),
        "addressDefault":addressDefault,
        "code":code,
        "discount":discount,
        "deliveryFee":deliveryFee,
        "message":message,
        "pretotal":pretotal
    }
def resovlePaymentAddress(request):
    request.session['payment_address']=request.POST.get('address')
    request.session['payment_address_update']=True

def resolveDiscount(request):
    codeDiscount=request.POST.get("discount")
    discount=getDiscountByCode(codeDiscount)
    if(discount != ""):
        request.session["discount"]=discount.discount
        request.session["code"]=discount.code
    
    

def resovelDiscountRemove(request):
    del request.session["discount"]





    