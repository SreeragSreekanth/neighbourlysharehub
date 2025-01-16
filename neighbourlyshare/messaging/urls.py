from django.urls import path
from . import views

urlpatterns = [
    path('conversation/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('inbox/', views.message_inbox, name='message_inbox'),
    path('send_message/<int:receiver_id>/', views.send_message, name='send_message'),
    path('messages/unread-count/', views.unread_messages_count, name='unread_count'),  # Moved to Messaging app

]
