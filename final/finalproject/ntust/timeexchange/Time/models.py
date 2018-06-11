from django.db import models 
from django import forms 
from django.core.validators import MinLengthValidator 
from django.contrib.auth.models import User 
from django.db.models.signals import post_save 
from django.dispatch import receiver 

 
# Create your models here. 
class Profile(models.Model): 
	user = models.OneToOneField(User, on_delete=models.CASCADE) 
	birthday=models.DateField(blank=True,null=True) 
	GENDER_CHOICES = (('M', 'Male'),('F', 'Female')) 
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES) 
	remaintime = models.PositiveIntegerField(blank=True,null=True,default=120) 
	phonenumber=models.CharField(max_length=100,blank=True) 
	def __str__(self): 
		return self.user.username 
@receiver(post_save, sender=User) 
def create_or_update_user_profile(sender, instance, created, **kwargs): 
	if created: 
 		Profile.objects.create(user=instance) 
	instance.profile.save() 

  
class Seller(models.Model): 
	user=models.ForeignKey(User,on_delete=models.CASCADE) 
	coursename=models.CharField(max_length=100,null=True) 
	coursedescription=models.TextField(max_length=300,null=True) 
	coursevalue=models.PositiveIntegerField(blank=True,null=True) 
	contact=models.CharField(max_length=100)
	pub_date=models.DateTimeField(auto_now=True) 
	def __str__(self): 
		return str(self.id)+"-"+self.coursename 
		
class Buyer(models.Model): 
	profile=models.ForeignKey(Profile,on_delete=models.CASCADE) 
	course=models.ForeignKey(Seller,on_delete=models.CASCADE) 
	buyID=models.AutoField(primary_key=True) 
	buy_date=models.DateTimeField(auto_now=True) 
	def __str__(self): 
 		return str(self.buyID)