"""
Forms for designs app
"""
from django import forms
from .models import Design, Product


class DesignUploadForm(forms.ModelForm):
    """Form for uploading a new design"""
    
    image_file = forms.ImageField(
        label='File Desain',
        help_text='PNG atau JPG, maksimal 20MB',
        widget=forms.FileInput(attrs={
            'accept': 'image/png,image/jpeg',
            'class': 'hidden',
            'id': 'image-upload',
        })
    )
    
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple,
        label='Pilih Produk',
        help_text='Pilih satu atau lebih produk untuk desain ini',
    )
    
    class Meta:
        model = Design
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent',
                'placeholder': 'Nama desain Anda...',
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent',
                'placeholder': 'Deskripsi singkat tentang desain ini...',
                'rows': 3,
            }),
        }
        labels = {
            'title': 'Judul Desain',
            'description': 'Deskripsi (opsional)',
        }
