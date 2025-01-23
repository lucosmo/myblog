from django import forms
from django.utils.html import escape


class CommentForm(forms.Form):
    author = forms.CharField(
        max_length=60,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Your Name"}
        ),
    )
    email = forms.EmailField(
        max_length=150,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Your Email"}
        ),
    )
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Leave a comment!"}
        )
    )

    def clean_author(self):
        author = self.cleaned_data.get("author")
        return escape(author)

    def clean_body(self):
        body = self.cleaned_data.get("body")
        return escape(body)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        return escape(email)
