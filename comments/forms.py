from django import forms

from .models import Comment

class CommentForm(forms.ModelForm):
    username = forms.CharField(
        label='Your Name *',
        widget = forms.TextInput(attrs={
        'type': 'text',
        'name': 'username'
        }))
    email = forms.EmailField(
        label='Your Email *',
        widget = forms.TextInput(attrs={
        'type': 'email',
        'name': 'email'
        }))
    site_url = forms.URLField(
        label='Website URL',
        required=False,
        widget = forms.TextInput(attrs={
        'id': 'url',
        'type': 'url',
        'name': 'url'
        }),
    )
    content = forms.CharField(
        label='Your Comment *',
        widget=forms.Textarea(attrs={
            'name': 'comment',
        })
    )
    class Meta:
        model = Comment
        fields = ['username', 'email', 'site_url', 'content',]