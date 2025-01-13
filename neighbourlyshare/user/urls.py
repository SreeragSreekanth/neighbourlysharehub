
from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.Userdashboard,name="user"),
    path('review/edit/<int:id>/', views.edit_review, name='edit_review'),
    path('review/delete/<int:id>/', views.delete_review, name='delete_review'),
]
