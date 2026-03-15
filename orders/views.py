import json
from decimal import Decimal, InvalidOperation

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from core.models import UserBranch
from products.models import Category, Product

from .models import InternalOrder, InternalOrderItem


@login_required
def order_shop(request):
    categories = Category.objects.order_by('name')
    products = Product.objects.filter(active=True).select_related(
        'unit',
        'category',
        'branch',
    ).order_by('name')

    error = None
    success = None
    notes_value = ''
    user_branch = UserBranch.objects.filter(user=request.user).select_related('branch').first()
    if request.method == 'POST':
        notes_value = request.POST.get('notes', '').strip()
        items_json = request.POST.get('items_json', '').strip()

        if user_branch is None:
            error = 'Ο χρήστης δεν έχει συνδεδεμένο branch.'
        elif not items_json:
            error = 'Το καλάθι είναι κενό.'
        else:
            try:
                submitted_items = json.loads(items_json)
            except json.JSONDecodeError:
                error = 'Τα στοιχεία της παραγγελίας δεν είναι έγκυρα.'
            else:
                product_map = {product.id: product for product in products}
                order_items = []

                for raw_item in submitted_items:
                    raw_product_id = str(raw_item.get('product_id', '')).strip()
                    raw_quantity = str(raw_item.get('quantity', '')).strip()

                    try:
                        product_id = int(raw_product_id)
                        quantity = Decimal(raw_quantity)
                    except (TypeError, ValueError, InvalidOperation):
                        error = 'Υπάρχει μη έγκυρη ποσότητα σε κάποιο προϊόν.'
                        break

                    if quantity <= 0:
                        continue

                    product = product_map.get(product_id)
                    if product is None:
                        error = 'Κάποιο προϊόν δεν βρέθηκε.'
                        break

                    order_items.append({
                        'product': product,
                        'quantity': quantity,
                    })

                if not error and not order_items:
                    error = 'Πρόσθεσε τουλάχιστον ένα προϊόν στην παραγγελία.'

                if not error:
                    with transaction.atomic():
                        order = InternalOrder.objects.create(
                            branch=user_branch.branch,
                            notes=notes_value,
                            created_by=request.user,
                        )

                        InternalOrderItem.objects.bulk_create([
                            InternalOrderItem(
                                order=order,
                                product=item['product'],
                                quantity=item['quantity'],
                            )
                            for item in order_items
                        ])

                    return redirect(
                        f"{reverse('orders:order_shop')}?created={order.id}"
                    )

    created_order_id = request.GET.get('created')
    if created_order_id:
        success = f'Η παραγγελία #{created_order_id} καταχωρίστηκε επιτυχώς.'

    return render(request, 'orders/order_shop.html', {
        'categories': categories,
        'products': products,
        'error': error,
        'success': success,
        'notes_value': notes_value,
        'user_branch': user_branch.branch if user_branch else None,
    })


@login_required
def order_list(request):
    error = None
    success = None
    current_user_branch = UserBranch.objects.filter(user=request.user).select_related('branch').first()
    current_user_branch_id = current_user_branch.branch_id if current_user_branch else None

    if request.method == 'POST':
        order_id = request.POST.get('order_id', '').strip()
        new_status = request.POST.get('status', '').strip()

        try:
            order = InternalOrder.objects.get(id=order_id)
        except (InternalOrder.DoesNotExist, ValueError):
            error = 'Η παραγγελία δεν βρέθηκε.'
        else:
            valid_statuses = {choice[0] for choice in InternalOrder.STATUS_CHOICES}
            if new_status not in valid_statuses:
                error = 'Το status δεν είναι έγκυρο.'
            else:
                order.status = new_status
                order.save(update_fields=['status', 'updated_at'])
                return redirect(f"{reverse('orders:order_list')}?updated={order.id}")

    updated_order_id = request.GET.get('updated')
    if updated_order_id:
        success = f'Το status της παραγγελίας #{updated_order_id} ενημερώθηκε.'

    orders = InternalOrder.objects.select_related(
        'branch',
        'created_by',
    ).prefetch_related(
        'items__product__unit',
        'items__product__branch',
    ).order_by('-created_at')

    for order in orders:
        if current_user_branch and current_user_branch.branch.name in {'Αρτοποιείο', 'Ζαχαροπλαστείο'}:
            order.visible_items = [
                item for item in order.items.all()
                if item.product.branch_id == current_user_branch_id
            ]
        else:
            order.visible_items = list(order.items.all())

        order.relevant_items_count = sum(
            1
            for item in order.items.all()
            if item.product.branch_id == current_user_branch_id
        )
        order.visible_items_count = len(order.visible_items)

    return render(request, 'orders/order_list.html', {
        'orders': orders,
        'status_choices': InternalOrder.STATUS_CHOICES,
        'error': error,
        'success': success,
        'current_user_branch_id': current_user_branch_id,
        'current_user_branch': current_user_branch.branch if current_user_branch else None,
    })


@login_required
def order_mark_read(request, order_id):
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'error': 'Method not allowed.'}, status=405)

    order = get_object_or_404(InternalOrder, id=order_id)

    if order.status == 'unread':
        order.status = 'read'
        order.save(update_fields=['status', 'updated_at'])

    return JsonResponse({
        'ok': True,
        'status': order.status,
        'status_label': dict(InternalOrder.STATUS_CHOICES).get(order.status, order.status),
    })
