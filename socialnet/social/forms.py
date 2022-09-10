from django import forms
from .models import *
from django.forms import FileInput

class NewStatusPostForm(forms.ModelForm):
    content = forms.CharField(label='',widget=forms.Textarea(attrs={'rows': 4, 'placeholder': "What's on your mind?"}))
    image = forms.ImageField(label='Choose a file you wish to upload: ', required=False)

    class Meta:
        model = StatusPost
        fields = ['content', 'image']