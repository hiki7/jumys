from django.urls import path
from .views import (
    FollowUserView, ListFollowersView,
    ConnectionRequestView, ApproveConnectionView, DeclineConnectionView,
    ReferenceLetterCreateView, ReferenceLetterListView
)

urlpatterns = [
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow_user'),
    path('followers/<int:user_id>/', ListFollowersView.as_view(), name='list_followers'),
    path('connect/<int:user_id>/', ConnectionRequestView.as_view(), name='connection_request'),
    path('connect/approve/<int:connection_id>/', ApproveConnectionView.as_view(), name='approve_connection'),
    path('connect/decline/<int:connection_id>/', DeclineConnectionView.as_view(), name='decline_connection'),
    path('reference-letter/create/', ReferenceLetterCreateView.as_view(), name='create_reference_letter'),
    path('reference-letter/list/', ReferenceLetterListView.as_view(), name='list_reference_letters'),
]
