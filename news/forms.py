from django import forms


class NewsCommentForm(forms.Form):
    text = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "class": "form-control",
                "placeholder": "Напишите комментарий...",
            }
        ),
    )
