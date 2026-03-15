from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render

from products.models import branch

from .models import UserBranch


def _users_with_branch():
    users = User.objects.select_related('user_branch__branch').order_by('username')
    for user in users:
        user.assigned_branch = getattr(getattr(user, 'user_branch', None), 'branch', None)
    return users


@login_required
def home(request):
    return render(request, 'core/index.html')


@login_required
def users(request):
    return render(request, 'core/user_list.html', {'users': _users_with_branch()})


@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html')


@login_required
def user_add(request):
    error = None
    branches = branch.objects.order_by('name')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        branch_id = request.POST.get('branch', '').strip()
        is_active = request.POST.get('is_active') == 'on'
        is_superuser = request.POST.get('is_superuser') == 'on'

        if not username or not password or not branch_id:
            error = 'Παρακαλώ συμπληρώστε όλα τα πεδία.'
        elif User.objects.filter(username=username).exists():
            error = 'Το όνομα χρήστη υπάρχει ήδη.'
        else:
            selected_branch = get_object_or_404(branch, id=branch_id)
            user = User.objects.create_user(username=username, password=password)
            user.is_active = is_active
            user.is_superuser = is_superuser
            user.save()
            UserBranch.objects.create(user=user, branch=selected_branch)

            return render(request, 'core/user_list.html', {
                'users': _users_with_branch()
            })

    return render(request, 'registration/add_user.html', {
        'error': error,
        'branches': branches,
    })


@login_required
def user_edit(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)
    error = None
    branches = branch.objects.order_by('name')
    user_branch = getattr(user_obj, 'user_branch', None)

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        branch_id = request.POST.get('branch', '').strip()
        is_active = request.POST.get('is_active') == 'on'
        is_superuser = request.POST.get('is_superuser') == 'on'

        if not username or not branch_id:
            error = 'Παρακαλώ συμπληρώστε το όνομα χρήστη και το branch.'
        elif User.objects.filter(username=username).exclude(id=user_id).exists():
            error = 'Το όνομα χρήστη υπάρχει ήδη.'
        else:
            selected_branch = get_object_or_404(branch, id=branch_id)
            user_obj.username = username
            if password:
                user_obj.set_password(password)
            user_obj.is_active = is_active
            user_obj.is_superuser = is_superuser
            user_obj.save()

            UserBranch.objects.update_or_create(
                user=user_obj,
                defaults={'branch': selected_branch},
            )

            return render(request, 'core/user_list.html', {
                'users': _users_with_branch()
            })

    return render(request, 'registration/user_edit.html', {
        'user_obj': user_obj,
        'error': error,
        'branches': branches,
        'selected_branch_id': user_branch.branch_id if user_branch else '',
    })


@login_required
def user_delete(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)
    user_obj.delete()
    return render(request, 'core/user_list.html', {
        'users': _users_with_branch()
    })
