from django.urls import path
from .views import check_session
from .views import UserRegistrationView, LoginView, LogoutView


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('check-session/', check_session, name='check_session'),
    # Add more paths for other functionalities
]
