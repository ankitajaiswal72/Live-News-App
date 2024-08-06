from django.urls import path
from frontend import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name="Home"),
    path('next', views.loadcontent, name="Loadcontent"),
    path('map', views.map_view, name="MapView"),
    path('news_by_country', views.news_by_country, name="NewsByCountry"),
     path('feed/', views.feed, name='feed'),
    path('post_article/', views.post_article, name='post_article'),
    path('vote_article/', views.vote_article, name='vote_article'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
