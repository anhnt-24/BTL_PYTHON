from ..models import GeneralCategory
from .categoryService import *

def getAllGeneralCategory():
    return GeneralCategory.objects.all()

def getGeneralCategoryByID(id):
    return {
        "generalCategory":GeneralCategory.objects.get(id=id),
        "list":getAllCategoryByGeneralId(id)
    }

def getAllGeneralCategoryDetail():
    l=[]
    for generalCategory in getAllGeneralCategory():
         l.append(getGeneralCategoryByID(id=generalCategory.id))
    return l

