from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message
from .forms import MessageForm
from userauth.models import Register  # Reference your custom user model
from django.db.models import Q  # Import Q from django.db.models


@login_required
def send_message(request, receiver_id):
    receiver = get_object_or_404(Register, id=receiver_id)
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user  # Here, request.user will be an instance of Register
            message.receiver = receiver
            message.save()
            return redirect('message_inbox')
    else:
        form = MessageForm()

    return render(request, 'send_message.html', {'form': form, 'receiver': receiver})

@login_required
def message_inbox(request):
    # Fetch unique conversations involving the logged-in user
    conversations = (
        Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
        .values('sender', 'receiver')
        .distinct()
    )

    # Extract unique conversation partners
    conversation_partners = []
    for convo in conversations:
        partner_id = convo['sender'] if convo['sender'] != request.user.id else convo['receiver']
        partner = Register.objects.get(id=partner_id)
        if partner not in conversation_partners:  # Avoid duplicates
            conversation_partners.append(partner)

    return render(request, 'inbox.html', {'conversations': conversation_partners})



@login_required
def conversation_detail(request, conversation_id):
    partner = get_object_or_404(Register, id=conversation_id)
    
    # Fetch messages between the logged-in user and the selected partner
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=partner) | Q(sender=partner, receiver=request.user)
    ).order_by('timestamp')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = partner
            message.save()
            return redirect('conversation_detail', conversation_id=conversation_id)
    else:
        form = MessageForm()

    return render(request, 'conversation_detail.html', {
        'messages': messages,
        'form': form,
        'partner': partner
    })
