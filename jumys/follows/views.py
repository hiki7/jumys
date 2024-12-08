from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Follow, Connection, ReferenceLetter
from .serializers import FollowSerializer, ConnectionSerializer, ReferenceLetterSerializer
from users.models import CustomUser

class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowSerializer

    def post(self, request, user_id):
        followee = get_object_or_404(CustomUser, id=user_id)
        if followee == request.user:
            return Response({'detail': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)
        follow, created = Follow.objects.get_or_create(follower=request.user, followee=followee)
        if created:
            serializer = self.get_serializer(follow)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': 'You are already following this user.'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        followee = get_object_or_404(CustomUser, id=user_id)
        follow = Follow.objects.filter(follower=request.user, followee=followee).first()
        if not follow:
            return Response({'detail': 'You are not following this user.'}, status=status.HTTP_400_BAD_REQUEST)
        follow.delete()
        return Response({'detail': 'Unfollowed successfully.'}, status=status.HTTP_200_OK)

class ListFollowersView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Follow.objects.filter(followee_id=user_id)

class ConnectionRequestView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ConnectionSerializer

    def post(self, request, user_id):
        receiver = get_object_or_404(CustomUser, id=user_id)
        if receiver == request.user:
            return Response({'detail': 'You cannot connect with yourself.'}, status=status.HTTP_400_BAD_REQUEST)
        connection, created = Connection.objects.get_or_create(sender=request.user, receiver=receiver)
        if created:
            serializer = self.get_serializer(connection)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': 'Connection request already exists.'}, status=status.HTTP_400_BAD_REQUEST)

class ApproveConnectionView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ConnectionSerializer

    def post(self, request, connection_id):
        connection = get_object_or_404(Connection, id=connection_id, receiver=request.user)
        if connection.status != 'pending':
            return Response({'detail': 'Connection request is not pending.'}, status=status.HTTP_400_BAD_REQUEST)
        connection.status = 'accepted'
        connection.save()
        serializer = self.get_serializer(connection)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DeclineConnectionView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ConnectionSerializer

    def post(self, request, connection_id):
        connection = get_object_or_404(Connection, id=connection_id, receiver=request.user)
        if connection.status != 'pending':
            return Response({'detail': 'Connection request is not pending.'}, status=status.HTTP_400_BAD_REQUEST)
        connection.status = 'declined'
        connection.save()
        serializer = self.get_serializer(connection)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ReferenceLetterCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReferenceLetterSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ReferenceLetterListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReferenceLetterSerializer

    def get_queryset(self):
        return ReferenceLetter.objects.filter(recipient=self.request.user)


class RequestReferenceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        recipient = get_object_or_404(CustomUser, id=user_id)
        if recipient == request.user:
            return Response({'detail': 'You cannot request a reference from yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        reference, created = ReferenceLetter.objects.get_or_create(
            author=request.user, recipient=recipient, status='pending'
        )
        if not created:
            return Response({'detail': 'A reference request is already pending.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ReferenceLetterSerializer(reference)
        return Response(serializer.data, status=status.HTTP_201_CREATED)