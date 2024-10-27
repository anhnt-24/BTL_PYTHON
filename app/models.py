from django.contrib.auth.models import User
from django.db import models
from django.db import models
from django.utils import timezone
from .handlefunc import fileHdl
from django.core.files.storage import default_storage



class Customer(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    email = models.EmailField(max_length=255, unique=True,blank=True, null=True)
    name = models.CharField(max_length=255,default='Default',null=True,blank=True)
    phone = models.CharField(max_length=20,unique=True,blank=True, null=True)
    img=models.ImageField(default=None,upload_to=fileHdl,blank=True, null=True)
    birth = models.DateField(default=timezone.now)
    role = models.CharField(max_length=45, default='user')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='male')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True) 

    def save(self, *args, **kwargs):
        if self.pk:
            old_instance = Customer.objects.get(pk=self.pk)
            if old_instance.img and old_instance.img != self.img:
                if default_storage.exists(old_instance.img.path):
                    default_storage.delete(old_instance.img.path)
        super(Customer, self).save(*args, **kwargs)

class GeneralCategory(models.Model):
    name = models.CharField(max_length=45) 
    description = models.CharField(max_length=45, null=True,blank=True)  
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    img=models.ImageField(default=None,upload_to=fileHdl)
    nameImg=models.CharField(null=True,blank=True,max_length=50)
    def __str__(self) -> str:
        return f"{self.id}_{self.name}"

class Category(models.Model):
    name = models.CharField(max_length=255)
    general_category = models.ForeignKey(GeneralCategory, on_delete=models.CASCADE)  
    description = models.TextField( null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self) -> str:
        return f"{self.id}_{self.name}"


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)     
    name = models.CharField(max_length=255,db_index=True)
    description = models.TextField(null=True,blank=True)
    price = models.IntegerField(default=1)
    sold = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self) -> str:
        return f"{self.id}_{self.name[0:50]}"

class Color(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  
    color = models.CharField(max_length=45)
    img=models.ImageField(default=None,upload_to=fileHdl,null=True,blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class Size(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    size=models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

class Color_Size(models.Model):
    color=models.ForeignKey(Color,on_delete=models.CASCADE)
    size=models.ForeignKey(Size,on_delete=models.CASCADE)
    stock=models.IntegerField(null=True,blank=True)
    sold=models.IntegerField(default=0)

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.CharField(max_length=45, )
    phone = models.CharField(max_length=45)
    id_province = models.CharField(max_length=25, default='0')
    id_commune = models.CharField(max_length=25, default='0')
    id_district = models.CharField(max_length=25, default='0')
    province = models.CharField(max_length=45,)
    district = models.CharField(max_length=45,)
    commune = models.CharField(max_length=45,)
    detail = models.CharField(max_length=255,)
    default=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    color_size= models.ForeignKey(Color_Size, on_delete=models.CASCADE)  
    quantity = models.IntegerField()
    price = models.IntegerField()
    total = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    total = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    deliveryFee= models.IntegerField(default=0)
    code = models.CharField(max_length=50,null=True,blank=True,db_index=True) 
    created_at = models.DateTimeField(default=timezone.now)


class OrderItem(models.Model):
    STATUS_CHOICES = [
        ('Chờ xác nhận', 'Chờ xác nhận'),
        ('Đang xử lý', 'Đang xử lý'),
        ('Đang giao', 'Đang giao'),
        ('Giao thành công', 'Giao thành công'),
        ('Đã hủy', 'Đã hủy'),
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE) 
    color_size= models.ForeignKey(Color_Size, on_delete=models.CASCADE)  
    quantity = models.IntegerField()
    total = models.IntegerField()
    status= models.CharField(max_length=255,choices=STATUS_CHOICES,default='Chờ xác nhận')
    delivered_at=models.DateTimeField(auto_now=True)
    address = models.ForeignKey(ShippingAddress,on_delete=models.SET_NULL,null=True)
    receiver = models.CharField(max_length=45,null=True)
    phone = models.CharField(max_length=45,null=True)
    province = models.CharField(max_length=45,null=True)
    district = models.CharField(max_length=45,null=True)
    commune = models.CharField(max_length=45,null=True)
    detail = models.CharField(max_length=255,null=True)    



class Slider(models.Model):
    img=models.ImageField(upload_to=fileHdl)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Discount(models.Model):
    code=models.CharField(max_length=100)
    discount=models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
