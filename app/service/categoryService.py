from .productService import *
from ..models import Category

def getAllCategory():
    return Category.objects.all()

def getCategoryByID(id):
    return {
        "category":Category.objects.get(id=id),
        "list":geAllProductByCategoryID(id)
    }

def getCategoryDetail():
    l=[]
    for category in getAllCategory():
        l.append(getCategoryByID(id=category.id))
    return l


def getAllCategoryByGeneralId(id):
    l=[]
    general_categories=Category.objects.filter(general_category=id)
    for general_category in general_categories:
        l.append(getCategoryByID(general_category.id))
    return l