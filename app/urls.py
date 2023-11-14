from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="index"),
    path('create_post/', views.create_post, name='create_post'),
    path('bookmark_post/<int:post_id>/', views.bookmark_post, name='bookmark_post'),
    path('toggle-like/<int:post_id>/', views.toggle_like, name='toggle-like'),

    path('bookmark_page/', views.bookmarkpage, name="bookmarkpage"),

]