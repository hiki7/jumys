from django.urls import path
from .views import (
    FollowUserView, ListFollowersView,
    ConnectionRequestView, ApproveConnectionView, DeclineConnectionView,
    ReferenceLetterCreateView, ReferenceLetterListView, RequestReferenceView, ManageReferenceRequestView
)

urlpatterns = [
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow_user'),
    path('followers/<int:user_id>/', ListFollowersView.as_view(), name='list_followers'),
    path('connect/<int:user_id>/', ConnectionRequestView.as_view(), name='connection_request'),
    path('connect/approve/<int:connection_id>/', ApproveConnectionView.as_view(), name='approve_connection'),
    path('connect/decline/<int:connection_id>/', DeclineConnectionView.as_view(), name='decline_connection'),
    path('references/create/', ReferenceLetterCreateView.as_view(), name='create_reference_letter'),
    path('references/', ReferenceLetterListView.as_view(), name='list_reference_letters'),
    path('references/request/<int:user_id>/', RequestReferenceView.as_view(), name='request-reference'),
    path('references/manage/<int:reference_id>/<str:action>/', ManageReferenceRequestView.as_view(), name='manage-reference'),
]
