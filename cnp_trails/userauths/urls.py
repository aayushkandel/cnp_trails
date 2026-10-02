from django.urls import path
from userauths import views

app_name="userauths"
urlpatterns=[
    path("sign-up/", views.RegisterView, name="sign-up"),
    path("sign-in/", views.loginViewTemp, name="sign-in"),
    path("verify-otp/", views.verify_otp_view, name="verify-otp"),
    path("resend-otp/", views.resend_otp_view, name="resend-otp"),
    path("sign-out/", views.LogoutView, name="sign-out"),
    path('profile-update/' , views.profile_update, name="profile-update"),
]