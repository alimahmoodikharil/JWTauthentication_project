from django.urls import path
from .views import SignUpView, SignInView, UserView, LogoutView

urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('signin/', SignInView.as_view()),
    path('user/', UserView.as_view()),
    path('logout/', LogoutView.as_view()),
]