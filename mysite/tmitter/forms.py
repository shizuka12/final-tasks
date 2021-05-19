from django import forms

from .models import Tmeet

class TmeetForm(forms.ModelForm):
    class Meta:
        model = Tmeet
        fields = (
            'content',
        )
        widgets = {
            'content': forms.Textarea(
                attrs={'placeholder': 'ここに入力'}
            ),
        }
