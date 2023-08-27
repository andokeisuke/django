from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.urls import reverse, reverse_lazy
from .models import Member

class Index(TemplateView):
    template_name = "testapp/Index.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # はじめに継承元のメソッドを呼び出す

        context["foo"] = "bar"
        # 追加したいコンテキスト情報(取得したコンテキスト情報のキーのリストを設定)
        extra = {"extra": list(context.keys())}
        # コンテキスト情報のキーを追加
        context.update(extra)
        return context
    

class MemberCreateView(CreateView):
    model = Member
    fields = "__all__"
    success_url = reverse_lazy('list')

class MemberListView(ListView):
    model = Member
    paginate_by = 5

class MemberUpdateView(UpdateView):
    model = Member
    fields = ('name', 'age')
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('list')

class MemberDeleteView(DeleteView):
    model = Member
    success_url = reverse_lazy('list')