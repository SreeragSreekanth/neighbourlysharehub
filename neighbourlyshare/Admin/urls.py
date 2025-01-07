
from django.urls import path
from . import views

urlpatterns = [
    path('admindash/', views.AdminDashboard,name="admin"),
    path('valuatorlist/', views.Valuatorlist,name="valuatorlist"),
    path('valuatorlist/add', views.add_valuator,name="valuatoradd"),
    path('userlist/', views.Userlist,name="userlist"),
    path('userlist/add', views.adduser,name="useradd"),
    path('userlist/delete/<int:id>/', views.deleteuser, name="deleteuser"),
    path('valuatorlist/delete/<int:id>/', views.deletevaluator, name="deletevaluator"),
    path('userlist/edit/<int:id>/', views.edituser, name="edituser"),
    path('valuatorlist/edit/<int:id>/', views.editvaluator, name="editvaluator"),
   
]
