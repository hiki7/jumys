from django.urls import path
from .views import (
    FollowUserView,
    ListFollowersView,
    ConnectionRequestView,
    ManageConnectionView,
    ReferenceLetterCreateView,
    ReferenceLetterListView,
    RequestReferenceView,
    ManageReferenceRequestView,
    ListSeekersView
)

urlpatterns = [
    # Follow/Unfollow Users
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow_user'),
    path('followers/<int:user_id>/', ListFollowersView.as_view(), name='followers_list'),

    # Connection Management
    path('connections/request/<int:user_id>/', ConnectionRequestView.as_view(), name='connection_request'),
    path('connections/manage/<int:connection_id>/<str:action>/', ManageConnectionView.as_view(), name='manage_connection'),

    # Reference Letters
    path('references/create/', ReferenceLetterCreateView.as_view(), name='create_reference_letter'),
    path('references/list/', ReferenceLetterListView.as_view(), name='reference_letters_list'),
    path('references/request/<int:user_id>/', RequestReferenceView.as_view(), name='request_reference'),
    path('references/manage/<int:reference_id>/<str:action>/', ManageReferenceRequestView.as_view(), name='manage_reference'),
    path('seekers/', ListSeekersView.as_view(), name='list_seekers'),
]
