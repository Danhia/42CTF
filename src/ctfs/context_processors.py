from .models import Category

def cat_processor(request):
    cat = Category.objects.order_by('name')
    return {'cats' : cat}
