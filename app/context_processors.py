from .service.service import *
def global_images(request):
    try:
        customer=getCustomer(request)
        return {
            'userimg' : customer.img,
        }
    except Exception:
        pass
    return{}

def global_generalCategory(request):
    try:
        generalCategory=getAllGeneralCategory()
        return{
            'generalCategory':generalCategory,
        }
    except:
        pass
    return {}

def global_cartQuantity(request):
    try:
        l=len(getAllCartItemByUser(request))

        if(l<=0): 
            return {
                "cartQuantity":None
            }
        return {
            "cartQuantity": l
        }
    except:
        pass
    return {
                "cartQuantity":None
    }
