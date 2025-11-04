from django.urls import path
from . import views

app_name = 'feedback'

urlpatterns = [
    path('', views.story_list, name='story_list'),
    path('story/create/', views.story_create, name='story_create'),
    path('story/<slug:slug>/', views.story_detail, name='story_detail'),
    path('thanks/', views.submit_thanks, name='submit_thanks'),
    path('accounts/signup/', views.signup_view, name='signup'), 

]