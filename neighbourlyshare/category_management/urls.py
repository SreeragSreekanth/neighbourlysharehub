from django.urls import path
from . import views

urlpatterns = [
    path('category/', views.category_list, name="category_list"),  # List categories
    path('category/add/', views.category_add, name="category_add"),  # Add new category
    path('category/edit/<int:id>/', views.category_edit, name="category_edit"),  # Edit category
    path('category/delete/<int:id>/', views.category_delete, name="category_delete"),  # Delete category
    path('valuator/', views.ValuatorDashboard,name="valuator"),
    path('item-management/', views.item_management, name='item_management'),
    path('approve-item/<int:item_id>/', views.approve_item, name='approve_item'),
    path('approval-needed/', views.approval_needed, name='approval_needed'),
    path('view-item/<int:item_id>/', views.view_item, name='view_item'),
    path('reject-item/<int:item_id>/', views.reject_item, name='reject_item'),


]
