from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('add', views.add, name='add'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('<int:hhs_id>/', views.detail, name='detail'),
	path('accounts/login/',
		 auth_views.LoginView.as_view(template_name='hhs/login.html')),
#	path('accounts/', include('django.contrib.auth.urls')),
]
