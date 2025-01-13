from django.urls import path
from . import views

urlpatterns = [
    path('itemlist/', views.Displayitems,name="itemlist"),
    path('itemlist/additem/', views.additem,name="additem"),
    path('itemlist/deleteitem/<int:id>/', views.deleteitem,name="deleteitem"),
    path('item/<int:id>/', views.viewitem, name='viewitem'),
    path('item/edit/<int:id>/', views.edititem, name='edititem'),
    path('item/image/delete/<int:id>/', views.deleteitemimage, name='deleteitemimage'),
    path('explore/', views.item_listing, name='itemsearch'),

]
