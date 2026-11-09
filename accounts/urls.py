
from django.urls import include, path
from .views import RegisterView,LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView,TokenBlacklistView

app_name = 'accounts'

urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),

    #JWT Auth
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('logout/',TokenBlacklistView.as_view(),name='logout')
]
