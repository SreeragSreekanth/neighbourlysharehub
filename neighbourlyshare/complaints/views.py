from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Complaint
from itemlisting.models import Item
from complaints.forms import ComplaintForm
from notifications.models import Notification
from notifications.utils import create_notification

@login_required
def file_complaint(request):
    """Allows users to file a complaint about any issue."""
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.save()

            messages.success(request, 'Complaint submitted successfully.')
            return redirect('user')  # Redirect to 'user' (which is the name of your user dashboard)
        else:
            messages.error(request, 'Please provide valid information.')

    else:
        form = ComplaintForm()

    return render(request, 'file_complaint.html', {'form': form})




@login_required
def complaints_list(request):
    """Shows a list of pending complaints."""
    complaints = Complaint.objects.filter(status='pending').order_by('-created_at')
    return render(request, 'complaints_list.html', {'complaints': complaints})




@login_required
def resolve_complaint(request, complaint_id):
    """Allows a valuator to resolve a complaint and send a notification."""
    complaint = get_object_or_404(Complaint, id=complaint_id)

    if request.method == 'POST':
        complaint.status = 'resolved'
        complaint.resolved_by = request.user  # Assign the valuator who resolved the complaint
        complaint.save()

        # Create a notification for the user when the complaint is resolved
        create_notification(
            user=complaint.user,
            message=f"Your complaint '{complaint.title}' has been resolved by {request.user.username}.",
            notification_type=Notification.RESOLVED_COMPLAINT
        )

        messages.success(request, 'Complaint resolved successfully.')
        return redirect('complaints_list')

    return render(request, 'resolve_complaint.html', {'complaint': complaint})

@login_required
def resolved_complaints_list(request):
    """Shows a list of resolved complaints."""
    resolved_complaints = Complaint.objects.filter(status='resolved').order_by('-created_at')
    return render(request, 'resolved_complaints_list.html', {'resolved_complaints': resolved_complaints})