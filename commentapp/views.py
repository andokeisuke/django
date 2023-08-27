from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic import DetailView
from .forms import CreateForm, SearchForm
from django.db.models import Q
from django.urls import reverse_lazy
from .models import Comment
from django.core.exceptions import PermissionDenied

from .forms import SignupForm, LoginForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

#シンプルにTemplateのコンテキストを変更したいときに使うクラス
class Index(TemplateView):
    template_name = "commentapp/Index.html"
    def get_context_data(self, **kwargs):# コンテキストの内容を編集する関数
        context = super().get_context_data(**kwargs) # 現在のコンテキストを読み込む
        context["foo"] = "bar"# 追加したいコンテキスト情報(取得したコンテキスト情報のキーのリストを設定)
        extra = {"extra": list(context.keys())}
        context.update(extra) # コンテキスト情報のキーを追加
        return context
    
#モデルデータを登録するための汎用ビュー
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment # モデル名指定
    form_class = CreateForm #フォームの指定
    success_url = reverse_lazy('list') #登録後のリダイレクト先を指定

    def form_valid(self, form): #有効なフォームが来たときに実行
        form.instance.create_user = self.request.user #編集者はフォームで登録せずビュー内で設定する
        return super(CreateView, self).form_valid(form) #データを登録する
 
 #一覧表を表示するための汎用ビュー
class CommentListView(ListView):
    model = Comment # モデル名指定
    from_class = SearchForm #フォームの指定
    paginate_by = 5 #1ページあたり何件表示させるか

    def get_context_data(self, **kwargs):# コンテキストの内容を編集する関数
        context = super().get_context_data(**kwargs) # 現在のコンテキストを読み込む
        context['search_form'] = self.form # 現在の検索フォームの内容をコンテキストsearch formで渡す
        return context

    def get_queryset(self, **kwargs):# 入力された検索条件をもとに表示データを変更する（POSTされたときに実行される関数）
        queryset = super().get_queryset()# 現在のテーブルのデータを取得
        if self.request.user.is_authenticated:# ゲストユーザではないか（何かしらのアカウントでログインされている）
            queryset = queryset.filter(Q(create_user=self.request.user)|Q(is_public=True))#ログインユーザーのものもしくは公開設定されているものを抽出
        else:
            queryset = queryset.filter(is_public=True)#公開設定されているものを抽出

        self.form = form = SearchForm(self.request.GET or None)#検索フォームの情報を取得
        if form.is_valid():#検索フォームの情報が有効かチェック
            is_public = form.cleaned_data.get('is_public')#検索窓の公開設定に関する選択肢を取得
            if is_public:
                queryset = queryset.filter(is_public=is_public)#選択肢をもとにを抽出
            create_user = form.cleaned_data.get('create_user')#検索窓の作成者に関する選択肢を取得
            if create_user:
                queryset = queryset.filter(create_user=create_user)#選択肢をもとにを抽出
        return queryset
    
#データを更新するための汎用ビュー
class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment # モデル名指定
    form_class = CreateForm#フォームの指定
    template_name_suffix = '_update_form'#テンプレートファイル名の指定、デフォルトだとCreateViewとかぶる
    success_url = reverse_lazy('list') #更新後のリダイレクト先を指定

    def get_object(self, queryset=None):#筆者とユーザーが異なる際に403エラー(更新前に実行される関数)    
        comment = super().get_object()# 現在のテーブルより更新対象のデータを取得
        if self.request.user == comment.create_user:
            return comment
        else:
            raise PermissionDenied
        
#データを更新するための汎用ビュー
class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment # モデル名指定
    success_url = reverse_lazy('list')#削除後のリダイレクト先を指定

    def get_object(self, queryset=None):#筆者とユーザーが異なる際に403エラー(削除前に実行される関数)   
        comment = super().get_object()# 現在のテーブルより削除対象のデータを取得
        if self.request.user == comment.create_user:
            return comment
        else:
            raise PermissionDenied

#データの詳細を表示するための汎用ビュー
class CommentDetail(DetailView):
    model = Comment# モデル名指定

    def get_object(self, queryset=None):#記事が公開されていない、または筆者とユーザーが異なる際に403エラー(表示前に実行される関数)   
        comment = super().get_object()# 現在のテーブルより表示対象のデータを取得
        if comment.is_public or self.request.user == comment.create_user:
            return comment
        else:
            raise PermissionDenied


#サインアップするための汎用ビュー（ユーザの追加）
class MySignupView(CreateView):
    template_name = 'commentapp/signup.html'#テンプレートファイル指定
    form_class = SignupForm #フォームの指定
    success_url = reverse_lazy('list')#追加後のリダイレクト先を指定
    
    def form_valid(self, form):#ユーザの追加が成功したらそのアカウントでログイン（追加フォームが送られてきたときに実行）
        result = super().form_valid(form)
        user = self.object
        login(self.request, user)
        return result

#ログインするための汎用ビュー（既存ユーザがログインする場合）
class MyLoginView(LoginView):
    template_name = 'commentapp/login.html' #テンプレートファイル指定
    form_class = LoginForm #フォームの指定

#ログアウトするための汎用ビュー
class MyLogoutView(LogoutView):
    template_name = 'commentapp/logout.html' #テンプレートファイル指定
    
