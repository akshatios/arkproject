
# from django.urls import path,include
# from arkauth import views

# urlpatterns = [
#     path('signup/',views.signup,name='signup'),
#     path('login/',views.handlelogin,name='handlelogin'),
# ]

# arkauth/urls.py
from django.urls import path
from . import views
from .views import signup , ActivateAccountView , RequestResetEmailView

app_name = 'arkauth'  # Use the app_name namespace

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.handlelogin, name='handlelogin'),
    path('logout/', views.handlelogout, name='handlelogout'),
    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate'),
    path('request-reset-email/',views.RequestResetEmailView.as_view(), name='request-reset-email'),
    path('set-new-password/<uidb64>/<token>',views.SetNewPasswordView.as_view(), name='set-new-password'),
]
