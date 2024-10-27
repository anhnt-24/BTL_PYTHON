from .productService import *
from django.core.paginator import Paginator

def searchPro(request):
    order=request.GET.get("order") or ""
    field=request.GET.get("field") or ""
    search=request.GET.get("search")
    product=getAllProductBySearch(search,field,order)
    paginator = Paginator(product, 8)  # Show 10 results per page
    page_number = request.GET.get('page')
    page_product = paginator.get_page(page_number)
    # Pass both the search query and the page object to the template
    return {
        "product":page_product,
        "search":search,
        "pages":range(1,paginator.num_pages+1),
        "order":order,
        "field":field
    }
