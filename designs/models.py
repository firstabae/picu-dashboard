"""
Design and Product models for PICU Creator Dashboard
"""
import uuid
from django.db import models
from django.conf import settings


class Product(models.Model):
    """
    Base product model (e.g., Kaos Cotton Combed 30s, Hoodie, Mug)
    """
    CATEGORY_CHOICES = [
        ('apparel', 'Apparel'),
        ('merchandise', 'Merchandise'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('Nama Produk', max_length=100)
    description = models.TextField('Deskripsi', blank=True, null=True)
    category = models.CharField('Kategori', max_length=20, choices=CATEGORY_CHOICES, default='apparel')
    base_cost = models.DecimalField('Base Cost', max_digits=12, decimal_places=2)
    is_active = models.BooleanField('Aktif', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Design(models.Model):
    """
    Design uploaded by creators
    """
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='designs',
        verbose_name='Creator'
    )
    title = models.CharField('Judul Desain', max_length=100)
    description = models.TextField('Deskripsi', blank=True, null=True)
    
    # Image will be stored in Supabase Storage
    # This field stores the URL/path to the image
    image = models.URLField('Image URL', max_length=500)
    
    # Status tracking
    status = models.CharField('Status', max_length=10, choices=STATUS_CHOICES, default='pending')
    reject_reason = models.TextField('Alasan Penolakan', blank=True, null=True)
    
    # Products this design is applied to
    products = models.ManyToManyField(
        Product,
        through='DesignProduct',
        related_name='designs',
        verbose_name='Products'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Design'
        verbose_name_plural = 'Designs'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} by {self.creator.full_name}"
    
    @property
    def is_pending(self):
        return self.status == 'pending'
    
    @property
    def is_approved(self):
        return self.status == 'approved'
    
    @property
    def is_rejected(self):
        return self.status == 'rejected'
    
    @property
    def status_badge_class(self):
        """Return CSS class for status badge"""
        return {
            'pending': 'bg-yellow-100 text-yellow-800',
            'approved': 'bg-green-100 text-green-800',
            'rejected': 'bg-red-100 text-red-800',
        }.get(self.status, '')
    
    @property
    def status_icon(self):
        """Return icon for status"""
        return {
            'pending': '🟡',
            'approved': '🟢',
            'rejected': '🔴',
        }.get(self.status, '')


class DesignProduct(models.Model):
    """
    Junction table for Design-Product relationship
    Each combination gets a unique SKU
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    design = models.ForeignKey(Design, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sku = models.CharField('SKU', max_length=30, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Design Product'
        verbose_name_plural = 'Design Products'
        unique_together = ['design', 'product']
    
    def save(self, *args, **kwargs):
        # Auto-generate SKU if not provided
        if not self.sku:
            design_short = str(self.design.id)[:4].upper()
            product_short = str(self.product.id)[:4].upper()
            self.sku = f"PICU-{design_short}-{product_short}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.sku}: {self.design.title} - {self.product.name}"
