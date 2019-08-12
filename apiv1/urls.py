from django.urls import path
from .views import UserProfileCreateView

urlpatterns = [
    path('user-profile/create/', UserProfileCreateView.as_view()),

]