from ..models import Product
from .colorService import *
from .sizeService import*
from .color_sizeService import *

def getAllProduct():
    return Product.objects.all()

def getProductByID(id):
    return {
           "product": Product.objects.get(id=id),
           "list":getAllColorByProductId(id=id)
    }

def getAllProductDetail():
    l=[]
    for product in getAllProduct():
        l.append(getProductByID(product=product.id))
    return l


def geAllProductByCategoryID(id):
    products=Product.objects.filter(category=id)
    l=[]
    for product in products:
        l.append(getProductByID(id=product.id))
    return l

def getProductByIDDetail(id):
    return {
           "product": Product.objects.get(id=id),
           "color":getAllColorByProductId(id=id),
           "size":getAllSizeByProductId(id),
           "c_s":getALLS_SByMTM(id)
    }

def getAllProductBySearch(search,field,order):
    
    if(order and field):
        sort=""
        if(order=="desc"):
            sort="-"
        products=Product.objects.filter(name__icontains=search).order_by(sort+field)
    else:
        products=Product.objects.filter(name__icontains=search)
    l=[]
    for item in products:
        l.append(getProductByIDDetail(item.id))

    return l
