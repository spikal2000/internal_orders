from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Product

def admin_required(view_func):
    decorated_view_func = login_required(user_passes_test(lambda u: u.is_superuser)(view_func))
    return decorated_view_func


@admin_required
def product_list(request):
    products = Product.objects.all().order_by('name')
    return render(request, 'products/products_list.html', {'products': products})


@admin_required
def product_add(request):
    error = None

    if request.method == 'POST':
        name = request.POST.get('name', "").strip()
        code = request.POST.get('code', "").strip() 
        description = request.POST.get('description', "").strip()
        # unit = request.POST.get('unit')
        active = request.POST.get('active') == 'on'

        if not name:
            error = "Το όνομα είναι υποχρεωτικό."
        elif not code and Product.objects.filter(code=code).exists():
            error = "Ο κωδικός είναι υποχρεωτικός και πρέπει να είναι μοναδικός."
        else:
            product = Product.objects.create(
                name=name,
                code=code,
                description=description,
                # unit=unit,
                active=active
            )
            return redirect('products:product_list')
    return render(request, 'products/product_add.html', {'error': error})

@admin_required
def product_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    error = None

    if request.method == 'POST':
        name = request.POST.get('name', "").strip()
        code = request.POST.get('code', "").strip() 
        description = request.POST.get('description', "").strip()
        # unit_id = request.POST.get('unit')
        active = request.POST.get('active') == 'on'

        if not name:
            error = "Το όνομα είναι υποχρεωτικό."
        elif not code and Product.objects.filter(code=code).exclude(id=product_id).exists():
            error = "Αυτος ο Κωδικός υπαρχει ήδη."
        else:
            product.name = name
            product.code = code
            product.description = description
            # product.unit_id = unit_id
            product.active = active
            product.save()
            return redirect('products:product_list')

    return render(request, 'products/products_list.html', {'product': product, 'error': error})


@admin_required
def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('products:product_list')

