# exchange/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import ExchangeRequest
from itemlisting.models import Item
from django.contrib.auth.decorators import login_required
from .forms import ExchangeRequestForm
from django.contrib import messages
from notifications.models import Notification
from userauth.decorators import role_required
from django.http import JsonResponse
from .models import ExchangeRequest





@login_required
@role_required(['user'])
def create_request(request, item_id):
    requested_item = get_object_or_404(Item, id=item_id)

    if request.method == 'POST':
        form = ExchangeRequestForm(request.POST, user=request.user)  # Pass user to the form
        if form.is_valid():
            exchange_request = form.save(commit=False)
            exchange_request.requested_item = requested_item
            exchange_request.offered_by = request.user
            exchange_request.save()

            # Create a notification for the item owner
            Notification.objects.create(
                user=requested_item.user,
                message=f"You have a new exchange request for your item {requested_item.title}",
                notification_type=Notification.NEW_MESSAGE
            )

            return redirect('request_list')
    else:
        form = ExchangeRequestForm(user=request.user)  # Pass user to the form

    return render(request, 'create_request.html', {
        'form': form,
        'requested_item': requested_item
    })



@login_required
@role_required(['user'])
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
            # Send notification to the user who requested the item
            Notification.objects.create(
                user=exchange_request.offered_by,
                message=f"Your exchange request for {exchange_request.requested_item.title} has been accepted.",
                notification_type=Notification.APPROVAL
            )
        elif action == 'decline':
            exchange_request.status = 'declined'
            # Send notification to the user who requested the item
            Notification.objects.create(
                user=exchange_request.offered_by,
                message=f"Your exchange request for {exchange_request.requested_item.title} has been declined.",
                notification_type=Notification.REJECTION
            )
        exchange_request.save()
        return redirect('incoming_requests')
    return render(request, 'respond_to_request.html', {'exchange_request': exchange_request})

@login_required
@role_required(['user'])
def request_list(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Sent requests
    user_requests = ExchangeRequest.objects.filter(offered_by=request.user).order_by('-created_at')

    # Received requests
    received_requests = ExchangeRequest.objects.filter(requested_item__user=request.user).order_by('-created_at')

    context = {
        'user_requests': user_requests,
        'received_requests': received_requests,
    }
    return render(request, 'request_list.html', context)


@login_required
@role_required(['user'])
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



@login_required
@role_required(['user'])
def approve_request(request, request_id):
    exchange_request = get_object_or_404(ExchangeRequest, id=request_id)
    if exchange_request.status == 'pending':
        exchange_request.status = 'accepted'
        exchange_request.save()
    return redirect('request_list')  # Redirect to the list of requests


@login_required
@role_required(['user'])
def reject_request(request, request_id):
    exchange_request = get_object_or_404(ExchangeRequest, id=request_id)
    if exchange_request.status == 'pending':
        exchange_request.status = 'declined'
        exchange_request.save()
    return redirect('request_list')  # Redirect to the list of requests


@login_required
@role_required(['user'])
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
            # Send notification to the user who created the request
            Notification.objects.create(
                user=exchange_request.offered_by,
                message=f"Your exchange request for {exchange_request.requested_item.title} has been accepted.",
                notification_type=Notification.APPROVAL
            )
        elif action == "reject":
            exchange_request.status = "declined"
            messages.info(request, "You have rejected the request.")
            # Send notification to the user who created the request
            Notification.objects.create(
                user=exchange_request.offered_by,
                message=f"Your exchange request for {exchange_request.requested_item.title} has been declined.",
                notification_type=Notification.REJECTION
            )
        exchange_request.save()

    return redirect('request_list')

@login_required
def get_new_requests_count(request):
    # Filter pending requests where the logged-in user owns the requested item
    count = ExchangeRequest.objects.filter(
        requested_item__user=request.user,  # Assuming 'user' is the owner field in the Item model
        status="pending"
    ).count()
    return JsonResponse({'unread_count': count})