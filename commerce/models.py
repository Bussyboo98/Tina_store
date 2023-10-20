from django.db import models

from django.contrib.auth.models import User

from django.conf import settings

from django.urls import reverse

from datetime import datetime

from tabnanny import verbose

# Create your models here.

class User(models.Model):
    user_name = models.CharField(max_length=200)
    user_email = models.EmailField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_name
    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=11)
    subject = models.CharField(max_length=50, default='complaint')
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta():
        verbose_name_plural = 'Contact Us'

    def __str__(self):
        return f"{self.email}"
    
class Shop(models.Model):
    product_name = models.CharField(max_length=200)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_image = models.FileField(blank=False, null=False, upload_to='store',verbose_name='Image')
    product_details = models.TextField()
    tag = models.CharField(max_length=10)
    slug = models.SlugField(max_length=250, unique=True)
    created = models.DateTimeField(auto_now_add =True)
    modified = models.DateTimeField(auto_now=True)

    class Meta():
        verbose_name_plural = "Store"

    def get_product_name(self):
        if self.product_name:
            return self.product_name
        
    def get_product_price(self):
        if self.product_price:
            return self.product_price
        
    def get_product_image(self):
        if self.product_image:
            return self.product_image
        
    def get_product_details(self):
        if self.product_details:
            return self.product_details
        
    def get_product_url(self):
        if self.product_name:
            return reverse('commerce:product_details', kwargs={'slug':self.slug})
        
    def __str__(self) -> str:
        return f"{self.product_name}"

class Payment(models.Model):
    name = models.CharField(max_length=50, null=True, blank=False)
    phone = models.CharField(max_length=11, blank=False)
    email = models.EmailField(max_length=100, blank=False)
    product_name = models.CharField(max_length=50, null=True)
    quantity = models.IntegerField(default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paystack_ref = models.CharField(max_length=15, blank=True)
    paid = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'payment {self.id}'
    
    @property
    def total_amount(self):
        return self.quantity * self.amount
    
    def get_quantity(self):
        if self.quantity:
            return self.quantity
    
    def get_amount(self):
        if self.amount:
            return self.amount * self.quantity
    
    def get_product(self):
        if self.product_name:
            return self.product_name
        
    def get_phone(self):
        if self.phone:
            return self.phone 
    
    def get_full_name(self):
        if self.name:
            return f'{self.name}'
