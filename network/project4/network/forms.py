from django import forms


class PostForm(forms.Form):
    postText = forms.CharField(label='New Post', max_length=140,widget=forms.Textarea(attrs={'class': 'form-control',"id":"postText"}))
    postText.widget.attrs.update(rows=3)