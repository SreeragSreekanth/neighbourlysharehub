from django.urls import path
from . import views

urlpatterns = [
    path('category/', views.category_list, name="category_list"),  # List categories
    path('category/add/', views.category_add, name="category_add"),  # Add new category
    path('category/edit/<int:id>/', views.category_edit, name="category_edit"),  # Edit category
    path('category/delete/<int:id>/', views.category_delete, name="category_delete"),  # Delete category
    path('valuator/assign/<int:item_id>/', views.assign_category, name="assign_category"),  # Assign categoryto an item
    path('valuator/', views.ValuatorDashboard,name="valuator"),

]
