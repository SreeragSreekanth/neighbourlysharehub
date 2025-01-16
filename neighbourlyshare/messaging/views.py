from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Message
from .forms import MessageForm
from userauth.models import Register
from django.db.models import Q
from notifications.utils import create_notification  # Import the utility to create notifications

@login_required
def send_message(request, receiver_id):
    receiver = get_object_or_404(Register, id=receiver_id)
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.save()
            
            # Create a notification for the receiver
            notification_message = f"You have a new message from {request.user.username}."
            create_notification(user=receiver, message=notification_message, notification_type="new_message")
            
            return redirect('message_inbox')
    else:
        form = MessageForm()

    return render(request, 'send_message.html', {'form': form, 'receiver': receiver})


@login_required
def message_inbox(request):
    conversations = (
        Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
        .values('sender', 'receiver')
        .distinct()
    )
    conversation_partners = []
    unread_messages_count = 0

    for convo in conversations:
        partner_id = convo['sender'] if convo['sender'] != request.user.id else convo['receiver']
        partner = Register.objects.get(id=partner_id)

        # Add partner to the list if not already present
        if partner not in conversation_partners:
            conversation_partners.append(partner)

        # Count unread messages for the partner in the conversation
        unread_count = Message.objects.filter(
            Q(sender=partner, receiver=request.user) | Q(sender=request.user, receiver=partner),
            read=False
        ).count()

        # Add to the total unread message count
        unread_messages_count += unread_count

        # Attach unread message count to the partner object
        partner.unread_messages = unread_count

    return render(request, 'inbox.html', {
        'conversations': conversation_partners,
        'unread_messages_count': unread_messages_count
    })



@login_required
def conversation_detail(request, conversation_id):
    partner = get_object_or_404(Register, id=conversation_id)

    # Fetch messages between the logged-in user and the selected partner
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=partner) | Q(sender=partner, receiver=request.user)
    ).order_by('timestamp')

    # Mark only received messages as read
    messages.filter(receiver=request.user, read=False).update(read=True)

    # Calculate unread count for the logged-in user
    unread_count = Message.objects.filter(
        receiver=request.user,
        read=False
    ).count()

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = partner
            message.save()

            # Redirect to the same page to show the new message
            return redirect('conversation_detail', conversation_id=conversation_id)
    else:
        form = MessageForm()

    return render(request, 'conversation_detail.html', {
        'messages': messages,
        'form': form,
        'partner': partner,
        'unread_count': unread_count,  # Pass the unread count to the template
    })




def unread_messages_count(request):
    if request.user.is_authenticated:
        # Changed is_read=False to read=False to match your model field name
        count = Message.objects.filter(receiver=request.user, read=False).count()
        return JsonResponse({'unread_count': count})
    return JsonResponse({'unread_count': 0})
