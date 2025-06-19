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
            'marriage_certificate',
        )
        for field in self.fields.values():
            field.widget.attrs['class'] = 'h-[55px] rounded-md text-black dark:text-white border border-gray-200 dark:border-[#172036] bg-white dark:bg-[#0c1427] px-[17px] block w-full outline-0 transition-all placeholder:text-gray-500 dark:placeholder:text-gray-400 focus:border-primary-500'

    class Meta:
        model = Tenant
        fields = ['full_name', 'id_type', 'id_number', 'tenant_numer', 'id_image', 'marriage_certificate']
        labels = {
            'full_name': 'الاسم الكامل',
            'id_type': 'نوع الهوية',
            'id_number': 'رقم الهوية',
            'tenant_numer': 'رقم الهاتف',
            'id_image': 'صورة الهوية',
            'marriage_certificate': 'صورة الشهادة',
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
            'marriage_certificate': forms.FileInput(attrs={
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

class UserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, label='الاسم الأول')
    last_name = forms.CharField(max_length=30, required=False, label='الاسم الأخير')
    phone = forms.CharField(max_length=15, label='رقم الهاتف')
    role = forms.ChoiceField(choices=[('admin', 'مدير'), ('receptionist', 'موظف استقبال')], label='الدور')
    password = forms.CharField(widget=forms.PasswordInput(), label='كلمة المرور')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'role', 'password']
        labels = {
            'first_name': 'الاسم الأول',
            'last_name': 'الاسم الأخير',
            'phone': 'رقم الهاتف',
            'role': 'الدور',
            'password': 'كلمة المرور',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set styling for all text input fields
        self.fields['first_name'].widget.attrs.update({
            'class': 'h-[55px] rounded-md text-black dark:text-white border border-gray-200 dark:border-[#172036] bg-white dark:bg-[#0c1427] px-[17px] block w-full outline-0 transition-all placeholder:text-gray-500 dark:placeholder:text-gray-400 focus:border-primary-500',
            'placeholder': 'مثال: أحمد محمد'
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'h-[55px] rounded-md text-black dark:text-white border border-gray-200 dark:border-[#172036] bg-white dark:bg-[#0c1427] px-[17px] block w-full outline-0 transition-all placeholder:text-gray-500 dark:placeholder:text-gray-400 focus:border-primary-500',
            'placeholder': 'مثال: علي'
        })
        self.fields['phone'].widget.attrs.update({
            'class': 'h-[55px] rounded-md text-black dark:text-white border border-gray-200 dark:border-[#172036] bg-white dark:bg-[#0c1427] px-[17px] block w-full outline-0 transition-all placeholder:text-gray-500 dark:placeholder:text-gray-400 focus:border-primary-500',
            'placeholder': 'مثال: +249 123 456 789'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'h-[55px] rounded-md text-black dark:text-white border border-gray-200 dark:border-[#172036] bg-white dark:bg-[#0c1427] px-[17px] block w-full outline-0 transition-all placeholder:text-gray-500 dark:placeholder:text-gray-400 focus:border-primary-500',
            'placeholder': 'أدخل كلمة المرور'
        })
        
        # Set the role field styling
        self.fields['role'].widget.attrs.update({
            'class': 'h-[55px] rounded-md border border-gray-200 dark:border-[#172036] bg-white dark:bg-[#0c1427] px-[13px] block w-full outline-0 cursor-pointer transition-all focus:border-primary-500'
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['phone']  # Set username as phone number
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            # Create or update profile
            Profile.objects.update_or_create(
                user=user,
                defaults={
                    'role': self.cleaned_data['role'],
                    'phone': self.cleaned_data['phone']
                }
            )
        return user

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, label='الاسم الأول')
    last_name = forms.CharField(max_length=30, required=False, label='الاسم الأخير')
    password = forms.CharField(widget=forms.PasswordInput(), required=False, label='كلمة المرور')
    role = forms.ChoiceField(choices=[('admin', 'مدير'), ('receptionist', 'موظف استقبال')], label='الدور')
    
    class Meta:
        model = Profile
        fields = ['phone', 'role']
        labels = {
            'phone': 'رقم الهاتف',
            'role': 'الدور',
        }
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'h-[55px] rounded-md text-black dark:text-white border border-gray-200 dark:border-[#172036] bg-white dark:bg-[#0c1427] px-[17px] block w-full outline-0 transition-all placeholder:text-gray-500 dark:placeholder:text-gray-400 focus:border-primary-500',
                'placeholder': 'مثال: +249 123 456 789'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'h-[55px] rounded-md text-black dark:text-white border border-gray-200 dark:border-[#172036] bg-white dark:bg-[#0c1427] px-[17px] block w-full outline-0 transition-all placeholder:text-gray-500 dark:placeholder:text-gray-400 focus:border-primary-500',
                'placeholder': 'اتركها فارغة للاحتفاظ بالكلمة الحالية'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # If editing existing user, populate User fields
            user = self.instance.user
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
        
        # Set the role field styling
        self.fields['role'].widget.attrs.update({
            'class': 'h-[55px] rounded-md border border-gray-200 dark:border-[#172036] bg-white dark:bg-[#0c1427] px-[13px] block w-full outline-0 cursor-pointer transition-all focus:border-primary-500'
        })
        
        # Set styling for first_name and last_name fields
        self.fields['first_name'].widget.attrs.update({
            'class': 'h-[55px] rounded-md text-black dark:text-white border border-gray-200 dark:border-[#172036] bg-white dark:bg-[#0c1427] px-[17px] block w-full outline-0 transition-all placeholder:text-gray-500 dark:placeholder:text-gray-400 focus:border-primary-500',
            'placeholder': 'مثال: أحمد محمد'
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'h-[55px] rounded-md text-black dark:text-white border border-gray-200 dark:border-[#172036] bg-white dark:bg-[#0c1427] px-[17px] block w-full outline-0 transition-all placeholder:text-gray-500 dark:placeholder:text-gray-400 focus:border-primary-500',
            'placeholder': 'مثال: علي'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'h-[55px] rounded-md text-black dark:text-white border border-gray-200 dark:border-[#172036] bg-white dark:bg-[#0c1427] px-[17px] block w-full outline-0 transition-all placeholder:text-gray-500 dark:placeholder:text-gray-400 focus:border-primary-500',
            'placeholder': 'اتركها فارغة للاحتفاظ بالكلمة الحالية'
        })

    def save(self, commit=True):
        profile = super().save(commit=False)
        
        if commit:
            # Update User fields
            user = profile.user
            user.first_name = self.cleaned_data.get('first_name', '')
            user.last_name = self.cleaned_data.get('last_name', '')
            
            # Update password if provided
            password = self.cleaned_data.get('password')
            if password:
                user.set_password(password)
            
            user.save()
            profile.save()
        
        return profile