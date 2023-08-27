from django.urls import path
from . import views          

urlpatterns = [
    path("",views.Index.as_view(), name="Index"),
    path('create/', views.MemberCreateView.as_view(), name='create'),
    path('list/', views.MemberListView.as_view(), name='list'),
    path('<int:pk>/update/', views.MemberUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.MemberDeleteView.as_view(), name='delete'),
    ]