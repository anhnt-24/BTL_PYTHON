from ..models import Color_Size

def getAllColor_Size():
    return Color_Size.objects.all()

def getColor_SizeByID(id):
    return Color_Size.objects.get(id=id)

def getColor_SizeByMTM(id1,id2):
    return Color_Size.objects.get(color=id1,size=id2)

