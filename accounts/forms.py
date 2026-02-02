"""
Custom forms for Django AllAuth and Profile
"""
from django import forms
from allauth.account.forms import SignupForm
from .models import User


class CustomSignupForm(SignupForm):
    """Extended signup form with custom fields"""
    
    full_name = forms.CharField(
        max_length=100,
        label='Nama Lengkap',
        widget=forms.TextInput(attrs={
            'placeholder': 'Nama Anda',
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg',
        })
    )
    
    phone = forms.CharField(
        max_length=20,
        label='No. WhatsApp',
        widget=forms.TextInput(attrs={
            'placeholder': '08123456789',
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg',
        })
    )
    
    instagram = forms.CharField(
        max_length=100,
        required=False,
        label='Link Instagram (opsional)',
        widget=forms.TextInput(attrs={
            'placeholder': 'https://instagram.com/username',
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg',
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Reorder fields so custom fields appear first
        field_order = ['full_name', 'email', 'phone', 'instagram', 'password1', 'password2']
        self.order_fields(field_order)
    
    def save(self, request):
        # Let adapter handle the save with custom fields
        user = super().save(request)
        return user


class ProfileForm(forms.ModelForm):
    """Form for editing user profile"""
    
    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone', 'instagram']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500',
                'readonly': 'readonly',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500',
            }),
            'instagram': forms.URLInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500',
                'placeholder': 'https://instagram.com/username',
            }),
        }
        labels = {
            'full_name': 'Nama Lengkap',
            'email': 'Email',
            'phone': 'No. WhatsApp',
            'instagram': 'Link Instagram',
        }


class BankInfoForm(forms.ModelForm):
    """Form for editing bank information"""
    
    class Meta:
        model = User
        fields = ['bank_name', 'bank_number', 'bank_holder']
        widgets = {
            'bank_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500',
                'placeholder': 'Contoh: BCA, BNI, Mandiri',
            }),
            'bank_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500',
                'placeholder': 'Nomor rekening',
            }),
            'bank_holder': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500',
                'placeholder': 'Nama sesuai buku tabungan',
            }),
        }
        labels = {
            'bank_name': 'Nama Bank',
            'bank_number': 'Nomor Rekening',
            'bank_holder': 'Atas Nama',
        }
