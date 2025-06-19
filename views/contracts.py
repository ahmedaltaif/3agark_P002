from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse
from Core.models.RentalContract import RentalContract
from Core.models.ContractTerms import ContractTerms
from P002.forms import RentalContractForm, TenantForm, ContractTermsForm
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from P002.utils import generate_contract_pdf
import os


def show(request):
    search_query = request.GET.get('search', '')
    contracts = RentalContract.objects.select_related('tenant', 'apartment', 'created_by').filter(status='active')
    
    if search_query:
        contracts = contracts.filter(
            Q(contract_num__icontains=search_query) |
            Q(tenant__full_name__icontains=search_query) |
            Q(apartment__unit_number__icontains=search_query) |
            Q(rent_price__icontains=search_query)
        )
    
    contracts = contracts.order_by('-contract_num')
    
    # Pagination
    paginator = Paginator(contracts, 10)  # Show 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'P002_contracts/show.html', {
        'contracts': page_obj,
        'page_obj': page_obj,
        'search_query': search_query,
    })


def archive(request):
    search_query = request.GET.get('search', '')
    contracts = RentalContract.objects.select_related('tenant', 'apartment', 'created_by').filter(status='expired')
    
    if search_query:
        contracts = contracts.filter(
            Q(contract_num__icontains=search_query) |
            Q(tenant__full_name__icontains=search_query) |
            Q(apartment__unit_number__icontains=search_query) |
            Q(rent_price__icontains=search_query)
        )
    
    contracts = contracts.order_by('-contract_num')
    
    # Pagination
    paginator = Paginator(contracts, 10)  # Show 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'P002_contracts/archive.html', {
        'contracts': page_obj,
        'page_obj': page_obj,
        'search_query': search_query
    })


def add(request):
    if request.method == 'POST':
        tenant_form = TenantForm(request.POST, request.FILES)
        contract_form = RentalContractForm(request.POST)

        if tenant_form.is_valid() and contract_form.is_valid():
            tenant = tenant_form.save()
            contract = contract_form.save(commit=False)
            contract.tenant = tenant
            contract.created_by = request.user  # Set the created_by field

            # Get the last contract with a non-null contract number
            last_contract = RentalContract.objects.exclude(contract_num__isnull=True).order_by('-contract_num').first()
            contract.contract_num = (last_contract.contract_num + 1) if last_contract else 1

            contract.save()
            return redirect('P002:contracts_show')  # make sure the name matches your urls
    else:
        tenant_form = TenantForm()
        contract_form = RentalContractForm()

    return render(request, 'P002_contracts/add.html', {
        'tenant_form': tenant_form,
        'contract_form': contract_form
    })


def view(request, contract_id):
    contract = get_object_or_404(RentalContract.objects.select_related('tenant', 'apartment', 'created_by'), id=contract_id)
    active_terms = ContractTerms.objects.filter(is_active=True).first()
    
    terms_list = []
    if active_terms:
        # Split content by newlines and filter out empty lines
        terms_list = [term.strip() for term in active_terms.content.split('\n') if term.strip()]
    
    if request.GET.get('pdf'):
        # Generate PDF
        pdf_path = generate_contract_pdf(contract, terms_list)
        return FileResponse(open(pdf_path, 'rb'), content_type='application/pdf')
    
    return render(request, 'P002_contracts/view.html', {
        'contract': contract,
        'terms': active_terms,
        'terms_list': terms_list
    })


def edit(request, contract_id):
    contract = get_object_or_404(RentalContract.objects.select_related('tenant'), id=contract_id)
    
    if request.method == 'POST':
        tenant_form = TenantForm(request.POST, request.FILES, instance=contract.tenant)
        contract_form = RentalContractForm(request.POST, instance=contract)
        
        if tenant_form.is_valid() and contract_form.is_valid():
            tenant_form.save()
            contract_form.save()
            messages.success(request, 'تم تحديث العقد بنجاح')
            return redirect('P002:contracts_show')
    else:
        tenant_form = TenantForm(instance=contract.tenant)
        contract_form = RentalContractForm(instance=contract)
    
    return render(request, 'P002_contracts/edit.html', {
        'tenant_form': tenant_form,
        'contract_form': contract_form,
        'contract': contract
    })


@login_required
def mark_expired(request, contract_id):
    contract = get_object_or_404(RentalContract, id=contract_id)
    contract.status = 'expired'
    contract.save()

    # Update apartment status
    apartment = contract.apartment
    apartment.is_occupied = False
    apartment.save()

    messages.success(request, 'تم تغيير حالة العقد إلى منتهي بنجاح')

    # Redirect to where the request came from
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('P002:contracts_show')
    return render(request, 'P002_contracts/archive.html', {'contract': contract})


@login_required
def terms_list(request):
    terms = ContractTerms.objects.all().order_by('-created_at')
    
    # Pagination
    paginator = Paginator(terms, 10)  # Show 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'P002_contracts/terms_list.html', {
        'terms': page_obj,
        'page_obj': page_obj,
    })

@login_required
def terms_add(request):
    if request.method == 'POST':
        form = ContractTermsForm(request.POST)
        if form.is_valid():
            # If this is marked as active, deactivate all other terms
            if form.cleaned_data['is_active']:
                ContractTerms.objects.all().update(is_active=False)
            form.save()
            messages.success(request, 'تم إضافة شروط العقد بنجاح')
            return redirect('P002:contracts_terms')
    else:
        form = ContractTermsForm()
    
    return render(request, 'P002_contracts/terms_form.html', {
        'form': form,
        'title': 'إضافة شروط عقد جديدة'
    })

@login_required
def terms_edit(request, terms_id):
    terms = get_object_or_404(ContractTerms, id=terms_id)
    
    if request.method == 'POST':
        form = ContractTermsForm(request.POST, instance=terms)
        if form.is_valid():
            # If this is marked as active, deactivate all other terms
            if form.cleaned_data['is_active']:
                ContractTerms.objects.exclude(id=terms_id).update(is_active=False)
            form.save()
            messages.success(request, 'تم تحديث شروط العقد بنجاح')
            return redirect('P002:contracts_terms')
    else:
        form = ContractTermsForm(instance=terms)
    
    return render(request, 'P002_contracts/terms_form.html', {
        'form': form,
        'title': 'تعديل شروط العقد'
    })

@login_required
def extend_contract(request, contract_id):
    contract = get_object_or_404(RentalContract.objects.select_related('tenant'), id=contract_id)
    
    if request.method == 'POST':
        # Only get the duration_days field from the form
        duration_days = request.POST.get('duration_days')
        if duration_days:
            try:
                contract.duration_days = int(duration_days)
                contract.save()
                messages.success(request, 'تم تمديد العقد بنجاح')
                return redirect('P002:apartments_occupied')
            except ValueError:
                messages.error(request, 'يرجى إدخال عدد صحيح للأيام')
    else:
        # Pre-fill the form with current duration
        initial_data = {'duration_days': contract.duration_days}
    
    return render(request, 'P002_contracts/extend.html', {
        'contract': contract,
        'initial_data': initial_data
    })


