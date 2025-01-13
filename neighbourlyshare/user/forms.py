from django.db import models
from userauth.models import Register
from django import forms
from .models import Rating
from userauth.models import Register
from itemlisting.models import Item,ItemImage

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating', 'review_text']
        widgets = {
            'rating': forms.Select(
                choices=[
                    (1, '1 - Very Poor'),
                    (2, '2 - Poor'),
                    (3, '3 - Average'),
                    (4, '4 - Good'),
                    (5, '5 - Excellent'),
                ],
                attrs={
                    'class': 'form-select',
                    'aria-label': 'Rating',
                }
            ),
            'review_text': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Leave your review...',
                }
            ),
        }
        labels = {
            'rating': 'Your Rating',
            'review_text': 'Your Review',
        }
        help_texts = {
            'rating': 'Select a rating from 1 (Very Poor) to 5 (Excellent).',
            'review_text': 'Write your detailed feedback here.',
        }
