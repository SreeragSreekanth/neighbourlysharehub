from notifications.models import Notification

def send_message(request, recipient_id):
    recipient = Register.objects.get(id=recipient_id)
    message_content = request.POST.get('message')
    
    # Save the message logic here...

    # Create a notification
    Notification.objects.create(
        user=recipient,
        message=f"You have a new message from {request.user.username}.",
        category='message'
    )
