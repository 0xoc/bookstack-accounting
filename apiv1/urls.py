from django.urls import path
from .views import *

urlpatterns = [
    path('user-profile/create/', UserProfileCreateView.as_view()),
    path('organization/create/', OrganizationCreateView.as_view()),
    path('user-profile/retrieve/', UserProfileRetrieveView.as_view()),
    path('organization/<int:organization_id>/staff/add/', OrganizationAddStaffView.as_view()),
]
