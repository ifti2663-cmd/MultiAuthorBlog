from django import forms
from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "featured_image",
            "category",
            "tags",
            "status",
        ]

        widgets = {
            "tags": forms.CheckboxSelectMultiple(),
        }