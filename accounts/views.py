"""
Views for accounts app
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileForm, BankInfoForm


@login_required
def profile(request):
    """View and edit user profile"""
    user = request.user
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil berhasil diperbarui!')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=user)
    
    context = {
        'form': form,
        'active_tab': 'profile',
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def bank_info(request):
    """Edit bank information for payouts"""
    user = request.user
    
    if request.method == 'POST':
        form = BankInfoForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Informasi bank berhasil diperbarui!')
            return redirect('accounts:bank_info')
    else:
        form = BankInfoForm(instance=user)
    
    context = {
        'form': form,
        'active_tab': 'bank',
    }
    return render(request, 'accounts/bank_info.html', context)
