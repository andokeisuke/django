from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic import DetailView
from .forms import CreateForm, SearchForm
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from .models import Comment

from .forms import SignupForm, LoginForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin


class Index(TemplateView):
    template_name = "commentapp/Index.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # はじめに継承元のメソッドを呼び出す

        context["foo"] = "bar"
        # 追加したいコンテキスト情報(取得したコンテキスト情報のキーのリストを設定)
        extra = {"extra": list(context.keys())}
        # コンテキスト情報のキーを追加
        context.update(extra)
        return context
    

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CreateForm
    success_url = reverse_lazy('list')

    def form_valid(self, form):
        form.instance.create_user = self.request.user
        return super(CreateView, self).form_valid(form)
 

class CommentListView( ListView):
    model = Comment
    from_class = SearchForm
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # search formを渡す
        context['search_form'] = self.form

        

        return context

    def get_queryset(self, **kwargs):

        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            queryset = queryset.filter(Q(create_user=self.request.user)|Q(is_public=True))
        else:
            queryset = queryset.filter(is_public=True)

        self.form = form = SearchForm(self.request.GET or None)

        if form.is_valid():
            is_public = form.cleaned_data.get('is_public')
            if is_public:
                queryset = queryset.filter(is_public=is_public)
            create_user = form.cleaned_data.get('create_user')
            if create_user:
                queryset = queryset.filter(create_user=create_user)
            


        return queryset
    

class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CreateForm
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('list')

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    success_url = reverse_lazy('list')

class CommentDetail(DetailView):
    model = Comment




#ログイン関連
class MySignupView(CreateView):
    template_name = 'commentapp/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('list')
    
    def form_valid(self, form):
        result = super().form_valid(form)
        user = self.object
        login(self.request, user)
        return result
    
class MyLoginView(LoginView):
    template_name = 'commentapp/login.html'
    form_class = LoginForm

class MyLogoutView(LogoutView):
    template_name = 'commentapp/logout.html'
    
