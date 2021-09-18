from django.urls import path

from polls import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('success/', views.success, name='success'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
