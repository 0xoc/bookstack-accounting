from django.urls import path
from .views import UserProfileCreateView, OrganizationCreateView

urlpatterns = [
    path('user-profile/create/', UserProfileCreateView.as_view()),
    path('organization/create', OrganizationCreateView.as_view())

]