from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_post, name='create_post'),
    path('my_posts/', views.my_posts, name='my_posts'),
    path('signup/', views.signup, name='signup'),
    path('search/', views.search_raw, name='search_raw'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('ssti/', views.ssti_demo, name='ssti_demo')
]
