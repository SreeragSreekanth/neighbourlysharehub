from django.urls import path
from . import views

urlpatterns = [
    path('itemlist/', views.Displayitems,name="itemlist"),
    path('itemlist/additem/', views.additem,name="additem"),
    path('itemlist/deleteitem/<int:id>/', views.deleteitem,name="deleteitem"),

]
