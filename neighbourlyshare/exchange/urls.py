# exchange/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('request/<int:item_id>/', views.create_request, name='create_request'),
    path('requests/incoming/', views.incoming_requests, name='incoming_requests'),
    path('requests/outgoing/', views.outgoing_requests, name='outgoing_requests'),
    path('request/<int:request_id>/respond/', views.respond_to_request, name='respond_to_request'),
    path('requests/', views.request_list, name='request_list'),
    path('requests/<int:request_id>/', views.request_detail, name='request_detail'),  # Add this
    path('requests/approve/<int:request_id>/', views.approve_request, name='approve_request'),
    path('requests/reject/<int:request_id>/', views.reject_request, name='reject_request'),
    path('requests/handle/<int:request_id>/', views.handle_request, name='handle_request'),
    path('requests/unread-count/', views.get_new_requests_count, name='new_requests_count'),

]
