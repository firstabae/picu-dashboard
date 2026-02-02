"""
Views for dashboard app
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from designs.models import Design, Product
from accounts.models import User


def index(request):
    """Landing page - redirect to dashboard if logged in"""
    if request.user.is_authenticated:
        if request.user.is_admin:
            return redirect('dashboard:admin_dashboard')
        return redirect('dashboard:dashboard')
    return render(request, 'dashboard/index.html')


@login_required
def dashboard(request):
    """Main dashboard view for creators"""
    user = request.user
    
    # Redirect admins to admin dashboard
    if user.is_admin:
        return redirect('dashboard:admin_dashboard')
    
    # Get design statistics for this user
    designs = Design.objects.filter(creator=user)
    
    stats = {
        'total': designs.count(),
        'approved': designs.filter(status='approved').count(),
        'pending': designs.filter(status='pending').count(),
        'rejected': designs.filter(status='rejected').count(),
    }
    
    # Get recent designs
    recent_designs = designs[:5]
    
    context = {
        'stats': stats,
        'recent_designs': recent_designs,
    }
    
    return render(request, 'dashboard/dashboard.html', context)


@login_required
def admin_dashboard(request):
    """Admin dashboard with pending reviews and stats"""
    user = request.user
    
    if not user.is_admin:
        return HttpResponseForbidden("Hanya admin yang bisa mengakses halaman ini.")
    
    # Get all designs
    all_designs = Design.objects.all()
    pending_designs = all_designs.filter(status='pending').order_by('-created_at')
    
    # Quick stats
    stats = {
        'total_creators': User.objects.filter(role='creator').count(),
        'total_designs': all_designs.count(),
        'total_products': Product.objects.filter(is_active=True).count(),
        'pending_reviews': pending_designs.count(),
        'approved_designs': all_designs.filter(status='approved').count(),
    }
    
    # Recent activity (last 10 designs)
    recent_designs = all_designs.order_by('-updated_at')[:10]
    
    context = {
        'stats': stats,
        'pending_designs': pending_designs[:10],
        'recent_designs': recent_designs,
    }
    
    return render(request, 'dashboard/admin_dashboard.html', context)
