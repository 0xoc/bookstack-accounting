from django.urls import path
from .views import *

urlpatterns = [
    path('user-profile/create/', UserProfileCreateView.as_view()),
    path('organization/create', OrganizationCreateView.as_view()),
    path('user-profile/retrieve/', UserProfileRetrieveDetail.as_view()),
    # path('user-profile/retrieve/<pk>', UserProfileRetrieveView.as_view()),
]
