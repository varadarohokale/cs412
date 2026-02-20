from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):

    image_url = forms.URLField(label="Image URL", required=True)

    class Meta:

        model = Post
        fields =  ['caption']
