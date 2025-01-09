from django import forms
from .models import Item, ItemImage

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description']

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

    # def clean_image(self):
    #     image = self.cleaned_data.get('image')
    #     if image:
    #         # Add any image validation you need here
    #         # For example, check file size, type, etc.
    #         return image
    #     return None