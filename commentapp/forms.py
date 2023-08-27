from django import forms
from .models import Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class CreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('create_user',)


class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj): # label_from_instance 関数をオーバーライド
         return obj.username # 表示したいカラム名を return

# SearchFormクラスを定義
class SearchForm(forms.Form):
        date = forms.ModelChoiceField(queryset=Comment.objects.none(), label='date',
                                     empty_label='選択してください',required = False)
        create_user = CustomModelChoiceField(queryset=User.objects.all(),required = False)
        is_public = forms.ChoiceField(choices = ((None , "----"), (True, "公開"), (False, "非公開")),required = False)
        #name = forms.CharField(label='name', max_length=50,required = False,)
        #age = forms.IntegerField(required = False)
        class Meta:
            model = Comment
            fields = ("date", "is_public" , "create_user" )



class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    pass