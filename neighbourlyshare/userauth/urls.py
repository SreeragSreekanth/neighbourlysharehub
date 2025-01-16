
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', views.Login),
    path('logout/', views.logout_view),
    path('signup/', views.userReg),
    path('', views.homeFun),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='password_reset.html'), 
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), 
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), 
         name='password_reset_confirm'),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), 
         name='password_reset_complete'),
]
