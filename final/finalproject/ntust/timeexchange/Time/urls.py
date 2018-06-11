
from django.conf.urls import url
from.import views

urlpatterns=[
	url(r'^$',views.home,name='home'),
	url(r'^register/$', views.register, name='register'),
	url(r'^login/$', views.login, name='login'),
	url(r'^logout/$', views.logout, name='logout'),
	#url(r'^saveaccount/$',views.saveaccount,name='saveaccount'),
	url(r'^goods/$', views.goods, name='goods'),

	
	url(r'^goodspost/$', views.savegoods, name='savegoods'),
	url(r'^transaction/$', views.transaction, name='transaction'),

	#url(r'^register/$',views.member_list,name='memberlist'),
	#url(r'^updatemember/$',views.update_member,name='updatemember'),

]
