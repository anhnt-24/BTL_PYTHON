from ..models import Size
from .colorService import getAllColorByProductId
from .color_sizeService import getColor_SizeByMTM

def getAllSize():
    return Size.objects.all()

def getSizeByID(id):
    return Size.objects.get(id=id)

def getAllSizeByProductId(id):
    return Size.objects.filter(product=id)

def getALLS_SByMTM(id):
    sizes=getAllSizeByProductId(id)
    spec=getAllColorByProductId(id)
    l=[]
    for i in sizes:
        for j in spec:
            l.append(getColor_SizeByMTM(i.id,j.id))
    return l


