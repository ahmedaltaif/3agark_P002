from django.shortcuts import render, redirect
from Core.models.RentalContract import RentalContract
from Core.models.Apartment import Apartment
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required

@login_required 
def show(request):
    search_query = request.GET.get('search', '')
    
    # Get total counts
    total_contracts = RentalContract.objects.filter(status='active').count()
    total_apartments = Apartment.objects.count()
    available_apartments = Apartment.objects.filter(is_occupied=False).count()
    occupied_apartments = Apartment.objects.filter(is_occupied=True).count()

    # Get recent contracts and apartments with search
    recent_contracts = RentalContract.objects.select_related('tenant', 'apartment', 'created_by')
    recent_apartments = Apartment.objects.all()

    if search_query:
        recent_contracts = recent_contracts.filter(
            Q(contract_num__icontains=search_query) |
            Q(tenant__full_name__icontains=search_query) |
            Q(apartment__unit_number__icontains=search_query) |
            Q(rent_price__icontains=search_query)
        )
        recent_apartments = recent_apartments.filter(
            Q(unit_number__icontains=search_query) |
            Q(unit_type__icontains=search_query) |
            Q(monthly_rent__icontains=search_query)
        )

    # Get only recent items
    recent_contracts = recent_contracts.order_by('-contract_num')[:5]
    recent_apartments = recent_apartments.order_by('-id')[:5]

    context = {
        'total_contracts': total_contracts,
        'total_apartments': total_apartments,
        'available_apartments': available_apartments,
        'occupied_apartments': occupied_apartments,
        'recent_contracts': recent_contracts,
        'recent_apartments': recent_apartments,
        'search_query': search_query,
    }
    return render(request, 'P002_home/show.html', context=context)