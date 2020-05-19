from django import forms
from .models import Comment
from snowpenguin.django.recaptcha3.fields import ReCaptchaField
# from django.contrib.auth.models import User

class CommentForm(forms.ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = Comment
        fields = ('name', 'email', 'body', 'captcha')
        widgets = {
            'name': forms.TextInput(attrs={'type': 'text', 'name': "name", 'placeholder': "Ваше имя", "value": "Аноним"}),
            'email': forms.TextInput(attrs={'type': 'email', 'name': "email", 'placeholder': "email"}),
            'body': forms.Textarea(attrs={'class': 'darma', 'name': "text", 'placeholder': "комментарий", 'id': 'contactcomment'}),
        }

    # def clean(self):

    #     data = self.cleaned_data
    #     # if "liwver@gmail.com" in data['email']:
    #     #     raise forms.ValidationError("YOU WILL BE ADMIN")
    #     if User.objects.filter(email=data['email']).exists():
    #         raise forms.ValidationError("YOU WILL BE ADMIN")

        # trial_start = data['trial_start']
        # movement_start = data['movement_start']
        # trial_stop = data['trial_stop']

        # if not (movement_start >= trial_start):
        #     raise forms.ValidationError('movement start must be >= trial start')

        # if not (trial_stop >= movement_start):
        #     raise forms.ValidationError('trial stop must be >= movement start')

        # if not (trial_stop > trial_start):
        #     raise forms.ValidationError('trial stop must be > trial start')

        # return data

    # def clean_name(self):
    #     clean_nam = self.cleaned_data['name']
    #     if "admin" or "Admin" or 'trini' in clean_nam:
    #         # print('ВЫ ДОЛЖНЫ ЗАЙТИ КАК АДМИН')
    #         raise forms.ValidationError("ВЫ ДОЛЖНЫ ЗАЙТИ КАК АДМИН")
    #     return self.cleaned_data['name']
    
    # def clean_email(self):
    #     clean_em = self.cleaned_data['email']
    #     if "liwver@gmail.com" in clean_em:
    #         # print('ВЫ ДОЛЖНЫ ЗАЙТИ КАК АДМИН')
    #         raise forms.ValidationError("ВЫ ДОЛЖНЫ ЗАЙТИ КАК АДМИН")
    #     return self.cleaned_data['email']












# <div class="col-lg-6 col-md-6 col-sm-12 form-group">
#     <input type="text" name="name" placeholder="Ваше имя" required>
# </div>

# <div class="col-lg-6 col-md-6 col-sm-12 form-group">
#     <input type="email" name="email" placeholder="Email" required>
# </div>

# <div class="col-lg-12 col-md-12 col-sm-12 form-group">
#     <textarea class="darma" name="text" placeholder="Ваше сообщение"></textarea>
# </div>