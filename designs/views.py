"""
Views for designs app
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Design, Product, DesignProduct
from .forms import DesignUploadForm


@login_required
def design_list(request):
    """List all designs for the current user (or all for admin)"""
    user = request.user
    
    if user.is_admin:
        designs = Design.objects.all()
    else:
        designs = Design.objects.filter(creator=user)
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter and status_filter in ['pending', 'approved', 'rejected']:
        designs = designs.filter(status=status_filter)
    
    context = {
        'designs': designs,
        'status_filter': status_filter,
    }
    
    return render(request, 'designs/list.html', context)


@login_required
def design_upload(request):
    """Upload a new design"""
    if request.method == 'POST':
        form = DesignUploadForm(request.POST, request.FILES)
        if form.is_valid():
            design = form.save(commit=False)
            design.creator = request.user
            
            # Handle file upload to Supabase Storage
            uploaded_file = request.FILES.get('image_file')
            if uploaded_file:
                # Upload to Supabase Storage (with local fallback)
                from picu.supabase_storage import upload_design_image
                image_url = upload_design_image(uploaded_file, str(request.user.id))
                design.image = image_url
            
            design.save()
            
            # Add selected products
            selected_products = form.cleaned_data.get('products')
            for product in selected_products:
                DesignProduct.objects.create(design=design, product=product)
            
            messages.success(request, f'Desain "{design.title}" berhasil diupload dan menunggu review.')
            return redirect('designs:list')
    else:
        form = DesignUploadForm()
    
    products = Product.objects.filter(is_active=True)
    
    context = {
        'form': form,
        'products': products,
    }
    
    return render(request, 'designs/upload.html', context)


@login_required
def design_detail(request, pk):
    """View design details"""
    design = get_object_or_404(Design, pk=pk)
    
    # Only allow creator or admin to view
    if not request.user.is_admin and design.creator != request.user:
        return HttpResponseForbidden("Anda tidak memiliki akses ke desain ini.")
    
    context = {
        'design': design,
        'design_products': design.designproduct_set.all(),
    }
    
    return render(request, 'designs/detail.html', context)


@login_required
def design_approve(request, pk):
    """Approve a design (admin only)"""
    if not request.user.is_admin:
        return HttpResponseForbidden("Hanya admin yang bisa approve desain.")
    
    design = get_object_or_404(Design, pk=pk)
    design.status = 'approved'
    design.reject_reason = None
    design.save()
    
    messages.success(request, f'Desain "{design.title}" berhasil di-approve.')
    return redirect('designs:detail', pk=pk)


@login_required
def design_reject(request, pk):
    """Reject a design (admin only)"""
    if not request.user.is_admin:
        return HttpResponseForbidden("Hanya admin yang bisa reject desain.")
    
    design = get_object_or_404(Design, pk=pk)
    
    if request.method == 'POST':
        reason = request.POST.get('reject_reason', '')
        design.status = 'rejected'
        design.reject_reason = reason
        design.save()
        
        messages.success(request, f'Desain "{design.title}" ditolak.')
        return redirect('designs:detail', pk=pk)
    
    return render(request, 'designs/reject_modal.html', {'design': design})


@login_required
def design_delete(request, pk):
    """Delete a design (creator only for their own designs, or admin)"""
    design = get_object_or_404(Design, pk=pk)
    
    # Check permission: only creator can delete their own design, or admin
    if not request.user.is_admin and design.creator != request.user:
        return HttpResponseForbidden("Anda tidak memiliki izin untuk menghapus desain ini.")
    
    if request.method == 'POST':
        design_title = design.title
        image_url = design.image
        
        # Delete design from database first
        design.delete()
        
        # Then try to delete associated image from storage
        if image_url:
            try:
                # Check if it's a Supabase URL (contains supabase.co or storage)
                if 'supabase' in image_url or '/storage/' in image_url:
                    from picu.supabase_storage import delete_design_image
                    deleted = delete_design_image(image_url)
                    if deleted:
                        messages.info(request, 'Gambar berhasil dihapus dari storage.')
                elif image_url.startswith('/media/'):
                    # Delete local file
                    import os
                    from django.conf import settings
                    local_path = os.path.join(settings.MEDIA_ROOT, image_url.replace('/media/', ''))
                    if os.path.exists(local_path):
                        os.remove(local_path)
            except Exception as e:
                import logging
                logging.warning(f"Failed to delete image from storage: {e}")
        
        messages.success(request, f'Desain "{design_title}" berhasil dihapus.')
        return redirect('designs:list')
    
    # GET request - show confirmation
    return render(request, 'designs/delete_confirm.html', {'design': design})


