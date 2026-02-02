"""
Custom User model for PICU Creator Dashboard
"""
import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Custom user manager for email-based authentication"""
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom User model for PICU Creator Dashboard
    Uses email as the primary identifier instead of username
    """
    
    ROLE_CHOICES = [
        ('creator', 'Creator'),
        ('admin', 'Admin'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None  # Remove username field
    email = models.EmailField('Email', unique=True)
    full_name = models.CharField('Nama Lengkap', max_length=100)
    phone = models.CharField('No. WhatsApp', max_length=20)
    instagram = models.CharField('Link Instagram', max_length=100, blank=True, null=True)
    
    # Bank information for payouts
    bank_name = models.CharField('Nama Bank', max_length=50, blank=True, null=True)
    bank_number = models.CharField('No. Rekening', max_length=30, blank=True, null=True)
    bank_holder = models.CharField('Atas Nama', max_length=100, blank=True, null=True)
    
    # Role (creator or admin)
    role = models.CharField('Role', max_length=10, choices=ROLE_CHOICES, default='creator')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'phone']
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        """Return the full_name field or email as fallback"""
        return self.full_name or self.email
    
    def get_short_name(self):
        """Return the first name or first part of email"""
        if self.full_name:
            return self.full_name.split()[0]
        return self.email.split('@')[0]
    
    @property
    def is_admin(self):
        return self.role == 'admin'
    
    @property
    def is_creator(self):
        return self.role == 'creator'
