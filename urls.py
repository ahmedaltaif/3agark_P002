from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from P002.views import home
from P002.views import contracts
from P002.views import apartments
from P002.views import auth
from P002.views import setting
from P002.views import users

app_name = 'P002'

urlpatterns = [
    # Home/Dashboard
    path('', home.show, name='home'),
    
    # Authentication
    path('logout/', auth.logout_view, name='logout'),
    
    # Apartments
    path('apartments/', apartments.show, name='apartments_show'),
    path('apartments/add/', apartments.add, name='apartments_add'),
    path('apartments/status/', apartments.status, name='apartments_status'),
    path('apartments/occupied/', apartments.occupied, name='apartments_occupied'),
    path('apartments/edit/<int:apartment_id>/', apartments.edit, name='apartments_edit'),
    path('apartments/confirm/<int:apartment_id>/', apartments.confirm, name='apartments_confirm'),
    path('apartments/pricing/', apartments.pricing, name='apartments_pricing'),
    path('apartments/pricing/<int:id>/edit/', apartments.edit_pricing, name='apartments_edit_pricing'),

    # Contracts
    path('contracts/', contracts.show, name='contracts_show'),
    path('contracts/add/', contracts.add, name='contracts_add'),
    path('contracts/<int:contract_id>/', contracts.view, name='contracts_view'),
    path('contracts/<int:contract_id>/edit/', contracts.edit, name='contracts_edit'),
    path('contracts/<int:contract_id>/extend/', contracts.extend_contract, name='contracts_extend'),
    path('contracts/<int:contract_id>/mark-expired/', contracts.mark_expired, name='contracts_mark_expired'),
    path('contracts/archive/', contracts.archive, name='contracts_archive'),
    
    # Contract Terms
    path('contracts/terms/', contracts.terms_list, name='contracts_terms'),
    path('contracts/terms/add/', contracts.terms_add, name='contracts_terms_add'),
    path('contracts/terms/<int:terms_id>/edit/', contracts.terms_edit, name='contracts_terms_edit'),

    # Users Management
    path('users/', users.show_users, name='users_show'),
    path('users/add/', users.add_user, name='users_add'),
    path('users/<int:user_id>/edit/', users.edit_user, name='users_edit'),
    path('users/<int:user_id>/delete/', users.confirm_delete_user, name='users_delete'),

    # Settings
    path('settings/', setting.show, name='settings_show'),

    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)