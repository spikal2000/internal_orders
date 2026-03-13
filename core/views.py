from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Create your views here.

@login_required
def home(request):
    return render(request, 'core/index.html')

@login_required
def users(request):
    users = User.objects.all().order_by('username')
    return render(request, 'core/user_list.html', {'users': users})


@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html')

@login_required
def user_add(request):
    error = None

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        is_active = request.POST.get('is_active') == 'on'
        is_superuser = request.POST.get('is_superuser') == 'on'

        if not username or not password:
            error = 'Παρακαλώ συμπληρώστε όλα τα πεδία.'
        elif User.objects.filter(username=username).exists():
            error = 'Το όνομα χρήστη υπάρχει ήδη.'
        else:
            user = User.objects.create_user(username=username, password=password)
            user.is_active = is_active
            user.is_superuser = is_superuser
            user.save()
            return render(request, 'core/user_list.html', {'users': User.objects.all().order_by('username')})

    return render(request, 'registration/add_user.html', {'error': error})



@login_required
def user_edit(request, user_id):
    user_obj = User.objects.get(id=user_id)
    error = None

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        is_active = request.POST.get('is_active') == 'on'
        is_superuser = request.POST.get('is_superuser') == 'on'

        if not username:
            error = 'Παρακαλώ συμπληρώστε το όνομα χρήστη.'
        elif User.objects.filter(username=username).exclude(id=user_id).exists():
            error = 'Το όνομα χρήστη υπάρχει ήδη.'
        else:
            user_obj.username = username
            if password:
                user_obj.set_password(password)
            user_obj.is_active = is_active
            user_obj.is_superuser = is_superuser
            user_obj.save()
            return render(request, 'core/user_list.html', {'users': User.objects.all().order_by('username')})
    
    return render(request, 'registration/user_edit.html', {'user_obj': user_obj, 'error': error})


@login_required
def user_delete(request, user_id):
    user_obj = User.objects.get(id=user_id)
    user_obj.delete()
    return render(request, 'core/user_list.html', {'users': User.objects.all().order_by('username')})

