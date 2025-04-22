from django import forms
from .models import Advisory

class AdvisoryForm(forms.ModelForm):
    class Meta:
        model = Advisory
        fields = ['title', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10, 'cols': 80}),
        }