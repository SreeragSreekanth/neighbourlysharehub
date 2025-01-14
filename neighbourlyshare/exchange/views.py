# exchange/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import ExchangeRequest
from itemlisting.models import Item
from django.contrib.auth.decorators import login_required
from .forms import ExchangeRequestForm
from django.contrib import messages
from notifications.models import Notification  # Import the Notification model



@login_required
def create_request(request, item_id):
    requested_item = get_object_or_404(Item, id=item_id)

    if request.method == 'POST':
        form = ExchangeRequestForm(request.POST, user=request.user)  # Pass user to the form
        if form.is_valid():
            exchange_request = form.save(commit=False)
            exchange_request.requested_item = requested_item
            exchange_request.offered_by = request.user
            exchange_request.save()
            return redirect('request_list')
    else:
        form = ExchangeRequestForm(user=request.user)  # Pass user to the form

    return render(request, 'create_request.html', {
        'form': form,
        'requested_item': requested_item
    })


@login_required
def incoming_requests(request):
    requests = ExchangeRequest.objects.filter(requested_item__user=request.user)
    return render(request, 'incoming_requests.html', {'requests': requests})

@login_required
def outgoing_requests(request):
    requests = ExchangeRequest.objects.filter(offered_by=request.user)
    return render(request, 'outgoing_requests.html', {'requests': requests})

@login_required
def respond_to_request(request, request_id):
    exchange_request = get_object_or_404(ExchangeRequest, id=request_id, requested_item__user=request.user)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'accept':
            exchange_request.status = 'accepted'
        elif action == 'decline':
            exchange_request.status = 'declined'
        exchange_request.save()
        return redirect('incoming_requests')
    return render(request, 'respond_to_request.html', {'exchange_request': exchange_request})



def request_list(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Sent requests
    user_requests = ExchangeRequest.objects.filter(offered_by=request.user)

    # Received requests
    received_requests = ExchangeRequest.objects.filter(requested_item__user=request.user)

    context = {
        'user_requests': user_requests,
        'received_requests': received_requests,
    }
    return render(request, 'request_list.html', context)



def request_detail(request, request_id):
    if not request.user.is_authenticated:
        return redirect('login')

    exchange_request = get_object_or_404(ExchangeRequest, id=request_id)

    # Ensure the user is either the requester or the owner of the requested item
    if (
        exchange_request.offered_by != request.user
        and exchange_request.requested_item.user != request.user
    ):
        return redirect('request_list')

    context = {
        'exchange_request': exchange_request,
    }
    return render(request, 'request_detail.html', context)




def approve_request(request, request_id):
    exchange_request = get_object_or_404(ExchangeRequest, id=request_id)
    if exchange_request.status == 'pending':
        exchange_request.status = 'accepted'
        exchange_request.save()
    return redirect('request_list')  # Redirect to the list of requests


def reject_request(request, request_id):
    exchange_request = get_object_or_404(ExchangeRequest, id=request_id)
    if exchange_request.status == 'pending':
        exchange_request.status = 'declined'
        exchange_request.save()
    return redirect('request_list')  # Redirect to the list of requests



def handle_request(request, request_id):
    if not request.user.is_authenticated:
        return redirect('login')

    exchange_request = get_object_or_404(ExchangeRequest, id=request_id)

    if exchange_request.requested_item.user != request.user:
        messages.error(request, "You are not authorized to take this action.")
        return redirect('request_list')

    if request.method == "POST":
        action = request.POST.get('action')
        if action == "accept":
            exchange_request.status = "accepted"
            messages.success(request, "You have accepted the request.")
        elif action == "reject":
            exchange_request.status = "declined"
            messages.info(request, "You have rejected the request.")
        exchange_request.save()

    return redirect('request_list')

def send_request(request, request_id):
    # Example where a user sends a request for an item
    exchange_request = ExchangeRequest.objects.get(id=request_id)
    recipient = exchange_request.offered_by  # The user who receives the request

    # Trigger a notification
    notification_message = f"You have a new exchange request for your item: {exchange_request.offered_item.title}"
    Notification.objects.create(
        user=recipient,
        message=notification_message,
        item=exchange_request.offered_item
    )

    # After the notification is created, render a response
    return render(request, 'request_sent.html', {'notification_message': notification_message})