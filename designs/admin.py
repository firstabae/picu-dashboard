"""
Django Admin configuration for Design models
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Design, DesignProduct


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin for Product model"""
    list_display = ('name', 'category', 'base_cost', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name',)
    ordering = ('name',)


class DesignProductInline(admin.TabularInline):
    """Inline for Design-Product relationship"""
    model = DesignProduct
    extra = 0
    readonly_fields = ('sku',)


@admin.register(Design)
class DesignAdmin(admin.ModelAdmin):
    """Admin for Design model"""
    list_display = ('title', 'creator_name', 'status_badge', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'creator__full_name', 'creator__email')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    inlines = [DesignProductInline]
    
    fieldsets = (
        ('Info Desain', {'fields': ('title', 'description', 'image', 'creator')}),
        ('Status', {'fields': ('status', 'reject_reason')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    
    def creator_name(self, obj):
        return obj.creator.full_name
    creator_name.short_description = 'Creator'
    
    def status_badge(self, obj):
        colors = {
            'pending': '#FCD34D',
            'approved': '#34D399',
            'rejected': '#F87171',
        }
        return format_html(
            '<span style="background-color: {}; padding: 4px 8px; border-radius: 4px;">{}</span>',
            colors.get(obj.status, '#9CA3AF'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'


@admin.register(DesignProduct)
class DesignProductAdmin(admin.ModelAdmin):
    """Admin for DesignProduct model"""
    list_display = ('sku', 'design', 'product', 'created_at')
    list_filter = ('product',)
    search_fields = ('sku', 'design__title')
    readonly_fields = ('sku',)
