from __future__ import unicode_literals
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.contrib.auth.models import User
from Time.forms import RegisterForm,ProfileForm,GoodsForm
from django.shortcuts import render, render_to_response,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login
from django.contrib import messages
import datetime
# Create your views here.
from . import models
from .models import Profile,Seller,Buyer

def home(request):
    return render(request,'homepage.html')
def register(request):
	if request.user.is_authenticated:
		member=Profile.objects.filter(user=request.user)
		return render(request,'register.html',{'member':member})
	else:
		if request.method == 'POST':
			user_form = RegisterForm(request.POST)
			profile_form = ProfileForm(request.POST)
			if user_form.is_valid() and profile_form.is_valid():
				user = user_form.save()
				user.refresh_from_db()
				profile_form = ProfileForm(request.POST,instance=user.profile)
				profile_form.full_clean()
				profile_form.save()
				messages.success(request,('Your account was successfully updated!'))
				return HttpResponseRedirect('/timeexchange/login/')
			else:
				messages.error(request,('Error,please fill out again'))
				return HttpResponseRedirect('/timeexchange/register/')
		else:
			user_form = RegisterForm(request.POST)
			profile_form = ProfileForm(request.POST)
		return render(request,'register.html',{
			'user_form': user_form,
			'profile_form': profile_form
			})
	
#    if request.method == 'POST':
#        form = Registerform(request.POST)
#        if form.is_valid():
#            user = form.save()
#           return HttpResponseRedirect('/timeexchange/login/')
#  else:
#        form = Registerform()
#    context = {'form':form}
#    return render(request,'register.html',context)
def login(request):
	if request.user.is_authenticated:
		return render(request,'login.html')
	else:
		if request.method == 'POST':
			username=request.POST.get('username','')
			password=request.POST.get('password','')
			user=auth.authenticate(username=username,password=password)
			if user is not None and user.is_active:
				auth.login(request,user)
				return render(request,'login.html')
			else:
				messages.error(request,('Please login again'))
				return render(request,'login.html')
	return render(request,'login.html')
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/timeexchange/login')

def goods(request): 
	if request.user.is_authenticated:#登入狀態
		goods=Seller.objects.all() 
		buyer=Profile.objects.filter(user=request.user)#顯示餘額在商品列表
		return render(request,'goods.html',{'goods':goods,'buyer':buyer})
	else:#未登入狀態
		goods2=Seller.objects.all() 
		return render(request,'goods.html',{'goods2':goods2})

def savegoods(request):
	if request.user.is_authenticated:
			if request.method == 'POST':
				goods_form=GoodsForm(request.POST)
				if goods_form.is_valid():
					member = User.objects.get(username=request.user)
					coursename=request.POST.get('coursename')
					coursedescription=request.POST.get('coursedescription')
					coursevalue=request.POST.get('coursevalue')
					contact=request.POST.get('contact')
					member.seller_set.create(contact=contact,coursename=coursename,coursedescription=coursedescription,coursevalue=coursevalue)
					messages.success(request,('Your goods was successfully published!'))
					return HttpResponseRedirect('/timeexchange/goodspost')	
				else:
					messages.error(request,('Error,please fill out again'))
					return render(request,'goodspost.html',{'goods_form':goods_form})
			else:
				goods_form=GoodsForm(request.POST)
				return render(request,'goodspost.html',{'goods_form':goods_form})
	else:
		messages.error(request,('Please login'))
		return HttpResponseRedirect('/timeexchange/login/')

def transaction(request):
	if request.user.is_authenticated:
		seller_id=request.GET['id']
		goods=Seller.objects.get(id=seller_id)
		seller=Profile.objects.get(user=goods.user)
		buyer=Profile.objects.get(user=request.user)
		if seller.user.id==buyer.user.id:
			messages.error(request,('Can not buy your own course'))
			return HttpResponseRedirect('/timeexchange/goods/')
		if buyer.remaintime<goods.coursevalue:
			messages.error(request,('Your remaintime is not enough'))
			return HttpResponseRedirect('/timeexchange/goods/')
		else:
			buyer.remaintime=buyer.remaintime-goods.coursevalue
			seller.remaintime=seller.remaintime+goods.coursevalue
			goods.delete()
			buyer.save()
			seller.save()
			messages.success(request,('You successfully bought this course'))
			return HttpResponseRedirect('/timeexchange/goods')
	else:
		messages.error(request,('Please login'))
		return HttpResponseRedirect('/timeexchange/login/')





def member_list(request):#顯示會員資料
	member=Profile.objects.filter(user=request.user)
	return render('register.html',{'member':member})
#還沒寫好不要裝def update_member(request):#修該會員資料
	if request.user.is_authenticated:
		if request.method == 'POST':
			member=User.objects.get(username=request.user)
			user_form = UpdateRegisterForm(request.POST,instance=member)
			profile_form = UpdateProfileForm(request.POST,instance=user.profile)
			if user_form.is_valid() and profile_form.is_valid():
				profile_form = UpdateProfileForm(request.POST, instance=user.profile)
				user_form.save()
				profile_form.save()
				messages.success(request,('Your account was successfully established!'))
				return HttpResponseRedirect('/timeexchange/login/')
			else:
				messages.error(request,('Please correct the error below.'))
				return HttpResponseRedirect('/timeexchange/register/')
		else:
			member=User.objects.get(username=request.user)
			user_form = UpdateRegisterForm(request.POST,instance=member)
			profile_form = UpdateProfileForm(request.POST,instance=member)
			return render(request,'updatemember.html',{
				'user_form': user_form,
				'profile_form': profile_form
				})
	else:
		return HttpResponseRedirect('/timeexchange/login/')
