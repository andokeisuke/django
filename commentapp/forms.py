from django import forms
from .models import Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class CreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('create_user',)#作成者以外を入力できるように設定

# 検索窓にて追加されたユーザが選択できるようにModelChoiceFieldを継承し、オーバーライド
class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj): # label_from_instance 関数をオーバーライド
         return obj.username # 表示したいカラム名を return

# SearchFormクラスを定義
class SearchForm(forms.Form):
        create_user = CustomModelChoiceField(queryset=User.objects.all(),required = False)
        is_public = forms.ChoiceField(choices = ((None , "----"), (True, "公開"), (False, "非公開")),required = False)
        class Meta:
            model = Comment
            fields = ("is_public" , "create_user" )

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    pass