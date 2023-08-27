from django.urls import path
from . import views          

urlpatterns = [
    path('create/', views.CommentCreateView.as_view(), name='create'),
    path('list/', views.CommentListView.as_view(), name='list'),
    path('<int:pk>/update/', views.CommentUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.CommentDeleteView.as_view(), name='delete'),
    path('<int:pk>/detail/',views.CommentDetail.as_view(),name='detail'),  

    path('signup/', views.MySignupView.as_view(), name='signup'),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', views.MyLogoutView.as_view(), name='logout'),

    ]