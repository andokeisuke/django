from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from .forms import CreateForm, SearchForm
from django.db.models import Q
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
    form_class = CreateForm
    success_url = reverse_lazy('list')

class MemberListView(ListView):
    model = Member
    from_class = SearchForm
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # search formを渡す
        context['search_form'] = self.form

        return context

    def get_queryset(self, **kwargs):

        queryset = super().get_queryset()
        self.form = form = SearchForm(self.request.GET or None)

        if form.is_valid():
            name = form.cleaned_data.get('name')
            if name:
                queryset = queryset.filter(name__icontains=name)

            age = form.cleaned_data.get('age')
            if isinstance(age, int):
                queryset = queryset.filter(age=age)

        return queryset

class MemberUpdateView(UpdateView):
    model = Member
    form_class = CreateForm
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('list')

class MemberDeleteView(DeleteView):
    model = Member
    success_url = reverse_lazy('list')