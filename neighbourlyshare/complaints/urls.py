from django.urls import path
from . import views

urlpatterns = [
    path('file_complaint/', views.file_complaint, name='file_complaint'),
    path('complaints/', views.complaints_list, name='complaints_list'),
    path('resolve_complaint/<int:complaint_id>/', views.resolve_complaint, name='resolve_complaint'),
    path('resolved_complaints/', views.resolved_complaints_list, name='resolved_complaints_list'),

]
