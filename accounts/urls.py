
from django.urls import include, path
from .views import RegisterView

app_name = 'accounts'

urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
]
