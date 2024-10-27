from ..models import OrderItem
from .shippingAddressService import getAddressById
def getOrderItemByID(id):
    return OrderItem.objects.get(id=id)

def getAllOrderItemByOrder(order):
    return OrderItem.objects.filter(order=order)

def getAllOderItemByStatus(status):
    return OrderItem.objects.filter(status=status)

def addOrderItem(order,color_size,quantity,total,address):
    orderItem=OrderItem(order=order)
    orderItem.color_size=color_size
    orderItem.quantity=quantity
    orderItem.total=total
    orderItem.address=address
    orderItem.receiver=address.receiver
    orderItem.phone=address.phone
    orderItem.detail=address.detail
    orderItem.commune=address.commune
    orderItem.district=address.district
    orderItem.province=address.province
    orderItem.save()
    
def deleteOrderItemByID(id):
    orderItem=OrderItem.objects.get(id=id)
    orderItem.status='Đã hủy'
    orderItem.save()

def updateOrderItemStatus(id):
    orderItem=OrderItem.objects.get(id=id)
    orderItem.status='Giao thành công'
    orderItem.save()

def changeOrderItemAddress(request,orderItemId):
    orderItem=getOrderItemByID(orderItemId)
    address=getAddressById(request.POST.get("address"))
    orderItem.address=address
    orderItem.receiver=address.receiver
    orderItem.phone=address.phone
    orderItem.detail=address.detail
    orderItem.commune=address.commune
    orderItem.district=address.district
    orderItem.province=address.province
    orderItem.save()

    
