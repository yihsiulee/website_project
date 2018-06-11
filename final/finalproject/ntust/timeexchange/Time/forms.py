from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,AnonymousUser 
from .models import Profile,Seller
import datetime


class RegisterForm(UserCreationForm):
	first_name = forms.CharField(max_length=30, required=False, help_text='')
	last_name = forms.CharField(max_length=30, required=False, help_text='')
	email = forms.EmailField(max_length=254, help_text='必填，請填入可使用的信箱')

	class Meta:
		model=User
		fields=('username', 'first_name', 'last_name', 'password1', 'password2',)

class ProfileForm(forms.ModelForm):
	birthday=forms.DateField(required=False,help_text='必填，格式：yyyy-mm-dd')
	GENDER_CHOICES = (('M','男'),('F','女'))
	gender = forms.ChoiceField(choices=GENDER_CHOICES)
	phonenumber=forms.CharField(max_length=100,required=False)

	class Meta:
		model=Profile
		fields=('birthday','gender','phonenumber')

class GoodsForm(ModelForm):
	contact=forms.CharField(help_text='LINE or email or another contact way')
	class Meta:
		model=Seller
		fields=('coursename','coursevalue','contact','coursedescription')
						