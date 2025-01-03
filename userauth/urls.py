
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.Login),
    path('signup/', views.userReg),
    path('', views.homeFun),
    path('about/', views.aboutUs),
    path('admindash/', views.AdminDashboard),
    path('user/', views.UserDashboard),
    path('valuator/', views.ValuatorDashboard),
]
