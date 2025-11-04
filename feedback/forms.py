from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['accuracy', 'bias', 'clarity', 'relevance', 'comment', 'anonymous', 'region']
        widgets = {
            'comment': forms.Textarea(attrs={'rows':4}),
            'region': forms.Select(),
        }

    def clean(self):
        cleaned = super().clean()
        # simple example: require comment if rating <=2 in any field
        low_rating = any(cleaned.get(f) and cleaned.get(f) <= 2 for f in ['accuracy','bias','clarity','relevance'])
        if low_rating and not cleaned.get('comment'):
            raise forms.ValidationError('Please explain why you chose a low rating in the comment field.')
        return cleaned