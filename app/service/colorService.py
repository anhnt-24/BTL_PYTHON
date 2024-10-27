from ..models import Color

def getAllColor():
    return Color.objects.all()

def getColorByID(id):
    return Color.objects.get(id=id)

def getAllColorByProductId(id):
    return Color.objects.filter(product=id)



