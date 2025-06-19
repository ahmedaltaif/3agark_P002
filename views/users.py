from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from P002.forms import UserUpdateForm, UserForm
from Core.models import Profile

@login_required
def show_users(request):
    # Get search query
    search_query = request.GET.get('search', '')
    
    # Get all users with their profiles, ordered by date joined
    users = User.objects.select_related('profile').all().order_by('-date_joined')
    
    # Apply search filter if query exists
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(profile__phone__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(users, 10)  # Show 10 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'users': page_obj,
        'search_query': search_query,
        'total_users': users.count(),
    }
    return render(request, 'P002_users/show.html', context=context)

@login_required
def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('P002:users_show')
    else:
        form = UserForm()
    context = {
        'form': form,
    }
    return render(request, 'P002_users/add.html', context=context)

@login_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    # Create profile if it doesn't exist
    profile, created = Profile.objects.get_or_create(user=user, defaults={
        'role': 'receptionist',
        'phone': user.username if user.username else ''
    })
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('P002:users_show')
    else:
        form = UserUpdateForm(instance=profile)
    context = {
        'form': form,
        'user': user,
    }
    return render(request, 'P002_users/edit.html', context=context)

@login_required
def confirm_delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('P002:users_show')
    return render(request, 'P002_users/confirm_delete.html', {'user': user})