"""
Custom adapter for Django AllAuth
"""
from allauth.account.adapter import DefaultAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):
    """Custom adapter to handle our custom User model fields"""
    
    def save_user(self, request, user, form, commit=True):
        """Save user with custom fields from signup form"""
        user = super().save_user(request, user, form, commit=False)
        
        # Get custom fields from form
        user.full_name = form.cleaned_data.get('full_name', '')
        user.phone = form.cleaned_data.get('phone', '')
        user.instagram = form.cleaned_data.get('instagram', '')
        user.role = 'creator'  # Default role for new signups
        
        if commit:
            user.save()
        
        return user
