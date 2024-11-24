from django.urls import path
from .views import SignUpView, SignInView, UserView, LogoutView, ForgetPasswordView, ResetPasswordView
urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('signin/', SignInView.as_view()),
    path('user/', UserView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('forget-password/', ForgetPasswordView.as_view()),
    path('reset-passowrd/<uid>/<token>/', ResetPasswordView.as_view(), name='reset_password'),
]