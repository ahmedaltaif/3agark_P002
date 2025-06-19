from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from P002.forms import UserForm

@login_required
@user_passes_test(lambda u: u.is_superuser)
def show(request):
    users = User.objects.all().select_related('profile')

    total_users = users.count()
    
    return render(request, 'P002_settings/show.html', {'users': users, 'total_users': total_users})