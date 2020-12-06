from django import forms
from nauta.models import Text, Category

MAX_LENGTH=50
class TextForm(forms.ModelForm):
    class Meta:
        model = Text
        fields = ['title', 'subtitle', 'author', 'text', 'categories', 'previous_post', 'next_post', 'firstchapter', 'nocopy', 'chapter']

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if len(title) > MAX_LENGTH:
            raise forms.ValidationError("title is too long! keep it simple.")
        return title

    def clean_subtitle(self):
        subtitle = self.cleaned_data.get("subtitle")
        if len(subtitle) > MAX_LENGTH:
            raise forms.ValidationError("subtitle is too long! keep it simple.")
        return subtitle

    def clean_author(self):
        author = self.cleaned_data.get("author")
        if len(author) > MAX_LENGTH:
            raise forms.ValidationError("author is too long! keep it simple.")
        return author