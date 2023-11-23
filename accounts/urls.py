from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.user_login, name="user_login"),
    path('register/', views.register, name='register'),
    path("logout/", views.user_logout, name="user_logout"),

    path('get_user_details/<int:user_id>/', views.get_user_details, name="get_user_details"),
    path('update_user_profile/<int:user_id>/', views.update_user_profile, name="update_user_profile"),

    path('forgot_password/', views.forgot_password, name="forgot_password"),
]