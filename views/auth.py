from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def logout_view(request):
    # Get user info before logout for displaying in template
    user_info = {
        'username': request.user.username,
        'full_name': request.user.get_full_name(),
    }
    
    if request.method == 'POST':
        # Perform logout
        logout(request)
        
        # Render logout template with user info
        return render(request, 'registration/logout.html', {'user_info': user_info})
    else:
        # If it's a GET request, show the logout confirmation page
        return render(request, 'registration/logout.html', {
            'user_info': user_info,
            'not_logged_out': True  # Flag to show different content
        }) 