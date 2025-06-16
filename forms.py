from django import forms
from Core.models import Apartment, Profile, Tenant, RentalContract, ContractTerms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML, Div

class ApartmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.template = 'crispy/layout.html'
        self.helper.field_template = 'crispy/field.html'
        self.helper.layout = Layout(
            'unit_number',
            'unit_type',
            'daily_rent',
            'weekly_rent',
            'monthly_rent',
            'is_occupied',
        )
        for field in self.fields.values():
            field.widget.attrs['class'] = 'h-[55px] rounded-md text-black dark:text-white border border-gray-200 dark:border-[#172036] bg-white dark:bg-[#0c1427] px-[17px] block w-full outline-0 transition-all placeholder:text-gray-500 dark:placeholder:text-gray-400 focus:border-primary-500'

    class Meta:
        model = Apartment
        fields = ['unit_number', 'unit_type', 'daily_rent', 'weekly_rent', 'monthly_rent', 'is_occupied']    
        labels = {
            'unit_number': 'رقم الوحدة',
            'unit_type': 'نوع الوحدة',
            'daily_rent': 'السعر اليومي',
            'weekly_rent': 'السعر الأسبوعي',
            'monthly_rent': 'السعر الشهري',
            'is_occupied': 'الحالة',
        }
        widgets = {
            'unit_number': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-50 h-[42px] text-sm rounded-md w-full block text-black pt-[11px] pb-[12px] px-[13px] placeholder:text-gray-500 outline-0 dark:bg-[#15203c] dark:text-white dark:border-[#15203c] dark:placeholder:text-gray-400'}),
            'unit_type': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-50 h-[42px] text-sm rounded-md w-full block text-black pt-[11px] pb-[12px] px-[13px] placeholder:text-gray-500 outline-0 dark:bg-[#15203c] dark:text-white dark:border-[#15203c] dark:placeholder:text-gray-400'}),
            'daily_rent': forms.NumberInput(attrs={'class': 'bg-gray-50 border border-gray-50 h-[42px] text-sm rounded-md w-full block text-black pt-[11px] pb-[12px] px-[13px] placeholder:text-gray-500 outline-0 dark:bg-[#15203c] dark:text-white dark:border-[#15203c] dark:placeholder:text-gray-400', 'step': '0.01', 'min': '0'}),
            'weekly_rent': forms.NumberInput(attrs={'class': 'bg-gray-50 border border-gray-50 h-[42px] text-sm rounded-md w-full block text-black pt-[11px] pb-[12px] px-[13px] placeholder:text-gray-500 outline-0 dark:bg-[#15203c] dark:text-white dark:border-[#15203c] dark:placeholder:text-gray-400', 'step': '0.01', 'min': '0'}),
            'monthly_rent': forms.NumberInput(attrs={'class': 'bg-gray-50 border border-gray-50 h-[42px] text-sm rounded-md w-full block text-black pt-[11px] pb-[12px] px-[13px] placeholder:text-gray-500 outline-0 dark:bg-[#15203c] dark:text-white dark:border-[#15203c] dark:placeholder:text-gray-400', 'step': '0.01', 'min': '0'}),
        }

class TenantForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.template = 'crispy/layout.html'
        self.helper.field_template = 'crispy/field.html'
        self.helper.layout = Layout(
            'full_name',
            'id_type',
            'id_number',
            'tenant_numer',
            'id_image',
        )
        for field in self.fields.values():
            field.widget.attrs['class'] = 'h-[55px] rounded-md text-black dark:text-white border border-gray-200 dark:border-[#172036] bg-white dark:bg-[#0c1427] px-[17px] block w-full outline-0 transition-all placeholder:text-gray-500 dark:placeholder:text-gray-400 focus:border-primary-500'

    class Meta:
        model = Tenant
        fields = ['full_name', 'id_type', 'id_number', 'tenant_numer', 'id_image']
        labels = {
            'full_name': 'الاسم الكامل',
            'id_type': 'نوع الهوية',
            'id_number': 'رقم الهوية',
            'tenant_numer': 'رقم الهاتف',
            'id_image': 'صورة الهوية',
        }
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'h-[55px] rounded-md text-black dark:text-white border border-gray-200 dark:border-[#172036] bg-white dark:bg-[#0c1427] px-[17px] block w-full outline-0 transition-all placeholder:text-gray-500 dark:placeholder:text-gray-400 focus:border-primary-500'
            }),
            'id_type': forms.Select(
                choices=[
                    ('جواز سفر', 'جواز سفر'),
                    ('رخصة', 'رخصة'),
                    ('رقم وطني', 'رقم وطني'),
                    ('بطاقة عسكرية', 'بطاقة عسكرية')
                ],
                attrs={
                    'class': 'h-[55px] rounded-md text-black dark:text-white border border-gray-200 dark:border-[#172036] bg-white dark:bg-[#0c1427] px-[17px] block w-full outline-0 transition-all placeholder:text-gray-500 dark:placeholder:text-gray-400 focus:border-primary-500'
                }
            ),
            'id_number': forms.TextInput(attrs={
                'class': 'h-[55px] rounded-md text-black dark:text-white border border-gray-200 dark:border-[#172036] bg-white dark:bg-[#0c1427] px-[17px] block w-full outline-0 transition-all placeholder:text-gray-500 dark:placeholder:text-gray-400 focus:border-primary-500'
            }),
            'tenant_numer': forms.TextInput(attrs={
                'class': 'h-[55px] rounded-md text-black dark:text-white border border-gray-200 dark:border-[#172036] bg-white dark:bg-[#0c1427] px-[17px] block w-full outline-0 transition-all placeholder:text-gray-500 dark:placeholder:text-gray-400 focus:border-primary-500'
            }),
            'id_image': forms.FileInput(attrs={
                'class': 'h-[55px] rounded-md text-black dark:text-white border border-gray-200 dark:border-[#172036] bg-white dark:bg-[#0c1427] px-[17px] block w-full outline-0 transition-all placeholder:text-gray-500 dark:placeholder:text-gray-400 focus:border-primary-500',
                'accept': 'image/*'
            }),
        }

class RentalContractForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.template = 'crispy/layout.html'
        self.helper.field_template = 'crispy/field.html'

        if not self.instance.pk:
            self.fields['apartment'].queryset = RentalContract.get_available_apartments()

        self.helper.layout = Layout(
            'apartment',
                Row(
                Column('rent_price', css_class='md:col-span-6'),
                Column('payment_method', css_class='md:col-span-6'),
                css_class='grid grid-cols-1 md:grid-cols-12 gap-[35px] mb-[35px]'
            ),
                Row(
                Column('checkin_date', css_class='md:col-span-6'),
                Column('issue_date', css_class='md:col-span-6'),
                css_class='grid grid-cols-1 md:grid-cols-12 gap-[35px] mb-[35px]'
            ),
                Row(
                Column('duration_days', css_class='md:col-span-6'),
                Column('status', css_class='md:col-span-6'),
                css_class='grid grid-cols-1 md:grid-cols-12 gap-[35px] mb-[35px]'
            ),
            'notes',
        )

        for field in self.fields.values():
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs['class'] = 'h-[140px] rounded-md text-black dark:text-white border border-gray-200 dark:border-[#172036] bg-white dark:bg-[#0c1427] p-[17px] block w-full outline-0 transition-all placeholder:text-gray-500 dark:placeholder:text-gray-400 focus:border-primary-500'
                field.widget.attrs['rows'] = 4
            else:
                field.widget.attrs['class'] = 'h-[55px] rounded-md text-black dark:text-white border border-gray-200 dark:border-[#172036] bg-white dark:bg-[#0c1427] px-[17px] block w-full outline-0 transition-all placeholder:text-gray-500 dark:placeholder:text-gray-400 focus:border-primary-500'

    class Meta:
        model = RentalContract
        fields = ['apartment', 'rent_price', 'payment_method', 'checkin_date', 'issue_date', 'duration_days', 'status', 'notes']
        labels = {
            'apartment': 'الوحدة السكنية',
            'rent_price': 'سعر الإيجار',
            'payment_method': 'طريقة الدفع',
            'checkin_date': 'تاريخ الدخول',
            'issue_date': 'تاريخ الإصدار',
            'duration_days': 'مدة العقد (بالأيام)',
            'status': 'حالة العقد',
            'notes': 'ملاحظات',
        }
        widgets = {
            'apartment': forms.Select(attrs={
                'class': 'h-[55px] rounded-md text-black dark:text-white border border-gray-200 dark:border-[#172036] bg-white dark:bg-[#0c1427] px-[17px] block w-full outline-0 transition-all placeholder:text-gray-500 dark:placeholder:text-gray-400 focus:border-primary-500'
            }),
            'rent_price': forms.NumberInput(attrs={
                'class': 'h-[55px] rounded-md text-black dark:text-white border border-gray-200 dark:border-[#172036] bg-white dark:bg-[#0c1427] px-[17px] block w-full outline-0 transition-all placeholder:text-gray-500 dark:placeholder:text-gray-400 focus:border-primary-500',
                'step': '0.01'
            }),
            'payment_method': forms.Select(
                choices=[('نقدي', 'نقدي'), ('بنكي', 'بنكي')],
                attrs={
                    'class': 'h-[55px] rounded-md text-black dark:text-white border border-gray-200 dark:border-[#172036] bg-white dark:bg-[#0c1427] px-[17px] block w-full outline-0 transition-all placeholder:text-gray-500 dark:placeholder:text-gray-400 focus:border-primary-500'
                }
            ),
            'checkin_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'h-[55px] rounded-md text-black dark:text-white border border-gray-200 dark:border-[#172036] bg-white dark:bg-[#0c1427] px-[17px] block w-full outline-0 transition-all placeholder:text-gray-500 dark:placeholder:text-gray-400 focus:border-primary-500',
                'dir': 'ltr'
            }),
            'issue_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'h-[55px] rounded-md text-black dark:text-white border border-gray-200 dark:border-[#172036] bg-white dark:bg-[#0c1427] px-[17px] block w-full outline-0 transition-all placeholder:text-gray-500 dark:placeholder:text-gray-400 focus:border-primary-500',
                'dir': 'ltr'
            }),
            'duration_days': forms.NumberInput(attrs={
                'class': 'h-[55px] rounded-md text-black dark:text-white border border-gray-200 dark:border-[#172036] bg-white dark:bg-[#0c1427] px-[17px] block w-full outline-0 transition-all placeholder:text-gray-500 dark:placeholder:text-gray-400 focus:border-primary-500'
            }),
            'status': forms.Select(
                choices=[('active', 'ساري'), ('expired', 'منتهي')],
                attrs={
                    'class': 'h-[55px] rounded-md text-black dark:text-white border border-gray-200 dark:border-[#172036] bg-white dark:bg-[#0c1427] px-[17px] block w-full outline-0 transition-all placeholder:text-gray-500 dark:placeholder:text-gray-400 focus:border-primary-500'
                }
            ),
            'notes': forms.Textarea(attrs={
                'class': 'h-[140px] rounded-md text-black dark:text-white border border-gray-200 dark:border-[#172036] bg-white dark:bg-[#0c1427] p-[17px] block w-full outline-0 transition-all placeholder:text-gray-500 dark:placeholder:text-gray-400 focus:border-primary-500',
                'rows': 4
            }),
        }

class ContractTermsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.template = 'crispy/layout.html'
        self.helper.field_template = 'crispy/field.html'
        self.helper.layout = Layout(
            'title',
            'content',
            'is_active',
        )
        for field in self.fields.values():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'h-[16px] w-[16px] rounded text-primary-500 border-gray-300 focus:ring-primary-500 dark:border-[#172036] dark:bg-[#0c1427] dark:checked:bg-primary-500 dark:focus:ring-offset-[#0c1427]'
            else:
                if isinstance(field.widget, forms.Textarea):
                    field.widget.attrs['class'] = 'h-[140px] rounded-md text-black dark:text-white border border-gray-200 dark:border-[#172036] bg-white dark:bg-[#0c1427] p-[17px] block w-full outline-0 transition-all placeholder:text-gray-500 dark:placeholder:text-gray-400 focus:border-primary-500'
                    field.widget.attrs['rows'] = 4
                else:
                    field.widget.attrs['class'] = 'h-[55px] rounded-md text-black dark:text-white border border-gray-200 dark:border-[#172036] bg-white dark:bg-[#0c1427] px-[17px] block w-full outline-0 transition-all placeholder:text-gray-500 dark:placeholder:text-gray-400 focus:border-primary-500'

    class Meta:
        model = ContractTerms
        fields = ['title', 'content', 'is_active']
        labels = {
            'title': 'عنوان الشروط',
            'content': 'محتوى الشروط',
            'is_active': 'نشط',
        }