# activity/forms.py
from django import forms
from .models import Activity

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = [
            'name',
            'description',
            'email',
            'image',
            'address',
            'status',
            'featured',
            'tags',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'address': forms.TextInput(attrs={'placeholder': 'Enter address'}),
        }

    def save(self, commit=True, partner=None):
        activity = super().save(commit=False)
        if partner:
            activity.partner = partner
        if commit:
            activity.save()
            self.save_m2m()
        return activity
