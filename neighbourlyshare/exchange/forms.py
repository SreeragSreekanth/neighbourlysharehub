from django import forms
from .models import ExchangeRequest
from itemlisting.models import Item  # Assuming the Item model is in the 'itemlisting' app

class ExchangeRequestForm(forms.ModelForm):
    class Meta:
        model = ExchangeRequest
        fields = ['offered_item', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write a message'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extract the user parameter
        super().__init__(*args, **kwargs)
        if user:
            # Filter the items to include only those owned by the logged-in user
            self.fields['offered_item'].queryset = Item.objects.filter(user=user,status='approved')