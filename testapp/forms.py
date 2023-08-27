from django import forms
from .models import Member

class CreateForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'


# SearchFormクラスを定義
class SearchForm(forms.Form):
        name = forms.CharField(label='name', max_length=50,required = False,)
        #age = forms.IntegerField(required = False)