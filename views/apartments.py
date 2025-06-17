from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from Core.models.Apartment import Apartment
from Core.models.RentalContract import RentalContract
from P002.forms import ApartmentForm  # Assuming you have a form for RentalContract
from django.db.models import Q
from django.contrib import messages


@login_required
def show(request):
    search_query = request.GET.get('search', '')
    apartments = Apartment.objects.all().order_by('unit_number')
    
    if search_query:
        apartments = apartments.filter(
            Q(unit_number__icontains=search_query) |
            Q(unit_type__icontains=search_query) |
            Q(monthly_rent__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(apartments, 10)  # Show 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'apartments': page_obj,
        'page_obj': page_obj,  # Add this for pagination template
        'search_query': search_query,
    }
    
    return render(request, 'P002_apartments/show.html', context=context)

@login_required
def add(request):
    if request.method == 'POST':
        apartment_form = ApartmentForm(request.POST)

        if apartment_form.is_valid():
            apartment = apartment_form.save(commit=False)
            apartment.created_by = request.user  # Assuming you have a created_by field
            apartment.save()
            return redirect('P002:apartments_show')  # adjust as needed
    else:
        apartment_form = ApartmentForm()
    context = {
        'apartment_form': apartment_form
    }

    return render(request, 'P002_apartments/add.html', context=context)

@login_required
def edit(request, apartment_id):
    apartment = Apartment.objects.get(id=apartment_id)
    if request.method == 'POST':
        apartment_form = ApartmentForm(request.POST, instance=apartment)
        if apartment_form.is_valid():
            apartment_form.save()
            return redirect('P002:apartments_show')
    else:
        apartment_form = ApartmentForm(instance=apartment)
    context = {
        'apartment_id': apartment_id,
        'apartment_form': apartment_form
    }
    return render(request, 'P002_apartments/edit.html', context=context)

@login_required
def confirm(request, apartment_id):
    try:
        apartment = Apartment.objects.get(id=apartment_id)
        
        if request.method == 'POST':
            apartment.delete()
            return redirect('P002:apartments_show')
            
        context = {
            'apartment': apartment
        }
        return render(request, 'P002_apartments/confirm.html', context=context)
        
    except Apartment.DoesNotExist:
        return redirect('P002:apartments_show')

@login_required
def status(request):
    # Get available apartments (not occupied)
    available_apartments = Apartment.objects.filter(is_occupied=False).order_by('unit_number')
    
    # Pagination
    paginator = Paginator(available_apartments, 10)  # Show 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'available_apartments': page_obj,
        'page_obj': page_obj,  # Add this for pagination template
    }
    
    return render(request, 'P002_apartments/apartments_status.html', context=context)

@login_required
def occupied(request):
    # Get occupied apartments with their active contracts
    occupied_apartments = []
    for apartment in Apartment.objects.filter(is_occupied=True):
        contract = RentalContract.objects.filter(apartment=apartment, status='active').first()
        if contract:
            apartment.active_contract = contract
            occupied_apartments.append(apartment)
    
    # Sort occupied apartments by contract end date
    occupied_apartments.sort(key=lambda x: x.active_contract.end_date)
    
    # Pagination
    paginator = Paginator(occupied_apartments, 10)  # Show 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'occupied_apartments': page_obj,
        'page_obj': page_obj,  # Add this for pagination template
    }
    
    return render(request, 'P002_apartments/occupied_apartments.html', context=context)

@login_required
def pricing(request):
    try:
        search_query = request.GET.get('search', '')
        apartments = Apartment.objects.all().order_by('unit_number')
        
        # Apply search filter if query exists
        if search_query:
            apartments = apartments.filter(
                Q(unit_number__icontains=search_query) |
                Q(unit_type__icontains=search_query) |
                Q(daily_rent__icontains=search_query) |
                Q(weekly_rent__icontains=search_query) |
                Q(monthly_rent__icontains=search_query)
            )
        
        # Pagination
        paginator = Paginator(apartments, 10)  # Show 10 items per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'apartments': page_obj,
            'page_obj': page_obj,
            'search_query': search_query
        }
        
        return render(request, 'P002_apartments/pricing.html', context)
    except Exception as e:
        print(f"DEBUG: Error in pricing view: {str(e)}")
        messages.error(request, 'حدث خطأ أثناء عرض صفحة الأسعار')
        return redirect('P002:home')

@login_required
def edit_pricing(request, id):
    apartment = get_object_or_404(Apartment, id=id)
    
    if request.method == 'POST':
        apartment.daily_rent = request.POST.get('daily_rent')
        apartment.weekly_rent = request.POST.get('weekly_rent')
        apartment.monthly_rent = request.POST.get('monthly_rent')
        apartment.save()
        messages.success(request, 'تم تحديث الأسعار بنجاح')
        return redirect('P002:apartments_pricing')
        
    return render(request, 'P002_apartments/edit_pricing.html', {'apartment': apartment})

@login_required
def archive_contract(request, contract_id):
    contract = get_object_or_404(RentalContract, id=contract_id)
    
    if request.method == 'POST':
        # Update contract status to expired
        contract.status = 'expired'
        contract.save()
        
        # Update apartment occupancy
        contract.apartment.is_occupied = False
        contract.apartment.save()
        
        messages.success(request, 'تم أرشفة العقد بنجاح')
        return redirect('P002:apartments_occupied')
    
    context = {
        'contract': contract
    }
    return render(request, 'P002_apartments/archive_contract.html', context)