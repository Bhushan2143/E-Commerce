from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Product(models.Model): 
     C=((1,'Mobile'),(2,'Shoes'),(3,'Cloth'))
     name=models.CharField(max_length=100)
     price=models.IntegerField()
     cat=models.IntegerField(verbose_name='Category',choices=C)
     pdetails=models.CharField(max_length=300, verbose_name='Product Details')
     is_active=models.BooleanField(default=True)
     pimage=models.ImageField(upload_to='image')

     def __str__(self):
          return self.name+self.pdetails

class Cart(models.Model):
     uid= models.ForeignKey('auth.User',on_delete= models.CASCADE,db_column='uid')
     pid= models.ForeignKey('Product',on_delete= models.CASCADE,db_column='pid')
     qty=models.IntegerField(default=1)

class Order(models.Model):
     uid= models.ForeignKey('auth.User',on_delete= models.CASCADE,db_column='uid')
     pid= models.ForeignKey('Product',on_delete= models.CASCADE,db_column='pid')
     qty= models.IntegerField(default=1)
     amt= models.IntegerField()