from ..models import Discount

def getDiscountByCode(code):
    try:
        res=Discount.objects.get(code=code)
        return res
    except:
        return ""