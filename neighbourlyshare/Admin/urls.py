
from django.urls import path
from . import views

urlpatterns = [
    path('adminDash/', views.AdminDashboard,name="admin"),
    path('adminDash/valuatorlist/', views.Valuatorlist,name="valuatorlist"),
    path('adminDash/valuatorlist/add', views.add_valuator,name="valuatoradd"),
    path('adminDash/userlist/', views.Userlist,name="userlist"),
    path('adminDash/userlist/delete/<int:id>/', views.deleteuser, name="deleteuser"),
    path('adminDash/valuatorlist/delete/<int:id>/', views.deletevaluator, name="deletevaluator"),
    path('admindash/userlist/edit/<int:id>/', views.edituser, name="edituser"),
    path('adminDash/valuatorlist/edit/<int:id>/', views.editvaluator, name="editvaluator"),
    path('adminDash/items/', views.adminitem, name="items"),
    path('adminDash/complaints', views.complaintlist,name="complaints"),
    path('adminDash/adminitemlist/viewitem<int:id>',views.admin_viewitem,name="adminview_item")
   
]
