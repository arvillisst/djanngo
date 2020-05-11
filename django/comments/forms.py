from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        widgets = {
            'name': forms.TextInput(attrs={'type': 'text', 'name': "name", 'placeholder': "Ваше имя", "value": "Аноним"}),
            'email': forms.TextInput(attrs={'type': 'email', 'name': "email", 'placeholder': "email"}),
            'body': forms.Textarea(attrs={'class': 'darma', 'name': "text", 'placeholder': "комментарий", 'id': 'contactcomment'}),
        }

# <div class="col-lg-6 col-md-6 col-sm-12 form-group">
#     <input type="text" name="name" placeholder="Ваше имя" required>
# </div>

# <div class="col-lg-6 col-md-6 col-sm-12 form-group">
#     <input type="email" name="email" placeholder="Email" required>
# </div>

# <div class="col-lg-12 col-md-12 col-sm-12 form-group">
#     <textarea class="darma" name="text" placeholder="Ваше сообщение"></textarea>
# </div>