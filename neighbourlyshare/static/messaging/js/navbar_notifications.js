
// Function to handle fetch errors
function handleFetchError(error) {
    console.error('Error fetching data:', error);
}

// Function to update badge visibility and content
function updateBadge(badge, count) {
    if (count > 0) {
        badge.style.display = 'inline';
        badge.textContent = count;
    } else {
        badge.style.display = 'none';
    }
}

// Function to update unread counts for messages, notifications, and requests
function updateUnreadCount() {
    const messageBadge = document.getElementById('message-badge');
    const notificationBadge = document.getElementById('notification-badge');
    const requestBadge = document.getElementById('request-badge');

    // Ensure badges exist before proceeding
    if (!messageBadge || !notificationBadge || !requestBadge) {
        console.error('Badge elements not found');
        return;
    }

    // Update unread messages count
    fetch('/messages/unread-count/')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => updateBadge(messageBadge, data.unread_count))
        .catch(handleFetchError);

    // Update unread notifications count
    fetch('/notifications/unread-count/')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => updateBadge(notificationBadge, data.unread_count))
        .catch(handleFetchError);

    // Update new requests count
    fetch('/requests/unread-count/')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => updateBadge(requestBadge, data.unread_count))
        .catch(handleFetchError);
}

// Call the function on page load
document.addEventListener('DOMContentLoaded', () => {
    updateUnreadCount();
    // Update counts every 30 seconds
    setInterval(updateUnreadCount, 30000);
});

