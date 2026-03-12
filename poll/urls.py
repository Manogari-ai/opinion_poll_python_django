# from django.contrib.auth import views as auth_views
# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.index, name='index'),
#     path('vote/<int:question_id>/', views.vote, name='vote'),
# ]

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [

    path('', views.index, name='index'),

    path('vote/<int:question_id>/', views.vote, name='vote'),

    path('register/', views.register, name='register'),

    path('login/', views.custom_login, name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('api/questions/', views.question_list_api),

    path('api/vote/', views.vote_api),

    path('api/login/', views.login_api),
    path('api/register/', views.register_api),
]