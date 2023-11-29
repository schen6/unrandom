from django.urls import path
from .views import UserRegistrationView
from .views import LoginView, LogoutView


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # Add more paths for other functionalities
]
