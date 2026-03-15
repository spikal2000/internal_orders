from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Category, Product, Unit, branch

def admin_required(view_func):
    decorated_view_func = login_required(user_passes_test(lambda u: u.is_superuser)(view_func))
    return decorated_view_func


@admin_required
def product_list(request):
    products = Product.objects.select_related('unit').all().order_by('name')
    return render(request, 'products/products_list.html', {'products': products})


@admin_required
def product_add(request):
    error = None
    Units = Unit.objects.all()
    Branches = branch.objects.all()
    Categories = Category.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name', "").strip()
        description = request.POST.get('description', "").strip()
        unit_id = request.POST.get('unit')
        unit = get_object_or_404(Unit, id=unit_id)
        branch_id = request.POST.get('branch')
        branch_obj = get_object_or_404(branch, id=branch_id)
        category_id = request.POST.get('category')
        category_obj = get_object_or_404(Category, id=category_id)
        active = request.POST.get('active') == 'on'

        if not name:
            error = "Το όνομα είναι υποχρεωτικό."
        else:
            product = Product.objects.create(
                name=name,
                description=description,
                unit=unit,
                branch=branch_obj,
                category=category_obj,
                active=active
            )
            return redirect('products:product_list')
    return render(request, 'products/product_add.html', {'error': error, 'units': Units, 'branches': Branches, 'categories': Categories})

@admin_required
def product_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    error = None
    Units = Unit.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name', "").strip()
        description = request.POST.get('description', "").strip()
        unit_id = request.POST.get('unit')
        unit = get_object_or_404(Unit, id=unit_id)
        active = request.POST.get('active') == 'on'

        if not name:
            error = "Το όνομα είναι υποχρεωτικό."
        else:
            product.name = name
            product.description = description
            product.unit = unit
            product.active = active
            product.save()
            return redirect('products:product_list')

    return render(request, 'products/product_edit.html', {'product': product, 'error': error, 'units': Units})


@admin_required
def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('products:product_list')




#------------------------------------ UNIT -------------------------------------------------

@admin_required
def unit_list(request):
    units = Unit.objects.all().order_by('name')
    return render(request, 'data/unit_list.html', {'units': units})


@admin_required
def unit_delete(request, unit_id):
    unit = get_object_or_404(Unit, id=unit_id)
    unit.delete()
    return redirect('products:unit_list')


@admin_required
def unit_add(request):
    error = None

    if request.method == 'POST':
        name = request.POST.get('name', "").strip()
        code = request.POST.get('code', "").strip()

        if not name or not code:
            error = "Το όνομα και ο κωδικός είναι υποχρεωτικά."
        elif Unit.objects.filter(code=code).exists():
            error = "Ο κωδικός υπάρχει ήδη."
        else:
            Unit.objects.create(name=name, code=code)
            return redirect('products:unit_list')

    return render(request, 'data/unit_add.html', {'error': error})



# ------------------------------------- BRANCH -------------------------------------------------

@admin_required
def branch_list(request):
    branches = branch.objects.all().order_by('name')
    return render(request, 'data/branch_list.html', {'branches': branches})

@admin_required
def branch_add(request):
    error = None

    if request.method == 'POST':
        name = request.POST.get('name', "").strip()

        if not name:
            error = "Το όνομα είναι υποχρεωτικό."
        else:
            branch.objects.create(name=name)
            return redirect('products:branch_list')

    return render(request, 'data/branch_add.html', {'error': error})

@admin_required
def branch_delete(request, branch_id):
    branch_obj = get_object_or_404(branch, id=branch_id)
    branch_obj.delete()
    return redirect('products:branch_list')



#------------------------------------- CATEGORY -------------------------------------------------
@admin_required
def category_list(request):
    categories = Category.objects.all().order_by('name')
    return render(request, 'data/categories_list.html', {'categories': categories})


@admin_required
def category_add(request):
    error = None

    if request.method == 'POST':
        name = request.POST.get('name', "").strip()

        if not name:
            error = "Το όνομα είναι υποχρεωτικό."
        else:
            Category.objects.create(name=name)
            return redirect('products:category_list')

    return render(request, 'data/category_add.html', {'error': error})

@admin_required
def category_delete(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect('products:category_list')




























