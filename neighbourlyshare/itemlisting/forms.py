from django import forms
from .models import Item, ItemImage
from category_management.models import Category


class ItemForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="Uncategorized",  # Displayed as the default option in the dropdown
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = Item
        fields = ['title', 'description', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set default value for the category field
        uncategorized = Category.objects.filter(name__iexact="Uncategorized").first()
        if uncategorized:
            self.fields['category'].initial = uncategorized
        
        # Add Bootstrap classes to the widgets explicitly
        self.fields['title'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter the title of the item'
        })
        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Provide a description for the item',
            'rows': 4  # You can adjust the height by adding the 'rows' attribute
        })
        self.fields['category'].widget.attrs.update({
            'class': 'form-control'
        })

class ItemImageForm(forms.ModelForm):
    image = forms.ImageField(
        required=False,  # Make the field optional
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'  # Restrict to image files
        })
    )

    class Meta:
        model = ItemImage
        fields = ['image']

class ItemSearchForm(forms.Form):
    q = forms.CharField(label='Search',required=False, widget=forms.TextInput(attrs={'placeholder': 'Search items...', 'class': 'form-control'}))
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    sort_by = forms.ChoiceField(
        choices=[('date_desc', 'Newest First'), ('date_asc', 'Oldest First'), ('title', 'Title')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )