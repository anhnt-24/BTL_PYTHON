from ..models import Order
from .orderItemService import *
from .userservice import getUser
from .paymentService import resolvePayment
from .messageService import *
from .shippingAddressService import getAllAddress,getAddressById
from ..handlefunc import generate_custom_uuid
from .cartService import deleteMultiCartItemByList
def getOrderByID(id):
    return Order.objects.get(id=id)

STATUS_CHOICES = [
         'Chờ xác nhận',
        'Đang xử lý',
        'Đang giao',
        'Giao thành công',
        'Đã hủy',
]

def getAllOrderByUser(request):
    l=[]
    user=getUser(request)
    order=Order.objects.filter(user=user).order_by("-created_at")
    for item in order:
        l+=getAllOrderItemByOrder(item)
    return l

def getOrderByStatus(request):
    l=[]
    order=getAllOrderByUser(request)
    
    for choice in STATUS_CHOICES:
       k=[]
       for item in order:
           if(item.status==choice): k.append(item)
       l.append(k) 
    return l


def getAllOrder(request):
    l=[getAllOrderByUser(request)]+getOrderByStatus(request)
    
    
    return{
        'order':l,
        'message':message(request),
        'address':getAllAddress(request)
    }
       
def createOrder(request):
    payment=resolvePayment(request)
    user=getUser(request)
    order=Order(user=user)
    order.total=payment['total']
    address=payment['addressDefault']
    discount=payment['discount']
    deliveryFee=payment['deliveryFee']
    order.deliveryFee=deliveryFee
    order.discount=discount or 0
    order.code=generate_custom_uuid(getUser(request).id)
    cartItem=request.session.get("cartItem[]") or []

    order.save()
    for item in payment['list']:
        addOrderItem(order,item['color_size'],item['quantity'],item['total_item'],address)
    if(discount != 0):
        del request.session['discount']
    if cartItem !=[]:
        deleteMultiCartItemByList(cartItem)
        del request.session['cartItem[]']
    del request.session['deliveryFee']
    del request.session['color_size']
    del request.session['quantity']
    del request.session['total']
    del request.session['item_total']
    request.session['message']="Đặt hàng thành công"

def deleteOrderItem(request,id):
    deleteOrderItemByID(id)
    request.session['message']='Hủy đơn hàng thành công'


def updateOrderStatus(request,id):
    updateOrderItemStatus(id)
    request.session['message']='Thành công'

def getOrderByCode(request):
    code=request.POST.get("code").strip()
    try:
        order=Order.objects.get(code=code)
        listOrderItem=getAllOrderItemByOrder(order)
        return {
            "order":order,
            "listOrderItem":listOrderItem,
        }
    except:
        return None




        
