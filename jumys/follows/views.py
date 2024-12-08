from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Follow, Connection, ReferenceLetter
from .forms import FollowForm, ConnectionRequestForm, ReferenceLetterForm
from users.models import CustomUser


# Follow/Unfollow Users
class FollowUserView(LoginRequiredMixin, View):
    def post(self, request, user_id):
        followee = get_object_or_404(CustomUser, id=user_id)
        if followee == request.user:
            messages.error(request, 'You cannot follow yourself.')
            return redirect('followers_list', user_id=user_id)

        follow, created = Follow.objects.get_or_create(follower=request.user, followee=followee)
        if created:
            messages.success(request, f'You are now following {followee.username}.')
        else:
            follow.delete()
            messages.success(request, f'You have unfollowed {followee.username}.')
        return redirect('followers_list', user_id=user_id)


# List Followers
class ListFollowersView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        followers = Follow.objects.filter(followee_id=user_id)
        return render(request, 'follows/followers_list.html', {'followers': followers})


# Connection Requests
class ConnectionRequestView(LoginRequiredMixin, View):
    def post(self, request, user_id):
        receiver = get_object_or_404(CustomUser, id=user_id)
        if receiver == request.user:
            messages.error(request, 'You cannot connect with yourself.')
            return redirect('connection_requests')

        form = ConnectionRequestForm({'receiver': receiver.id})
        if form.is_valid():
            connection, created = Connection.objects.get_or_create(sender=request.user, receiver=receiver)
            if created:
                messages.success(request, f'Connection request sent to {receiver.username}.')
            else:
                messages.error(request, 'Connection request already exists.')
        return redirect('connection_requests')


# Approve/Decline Connection Requests
class ManageConnectionView(LoginRequiredMixin, View):
    def post(self, request, connection_id, action):
        connection = get_object_or_404(Connection, id=connection_id, receiver=request.user)
        if action not in ['accept', 'decline']:
            messages.error(request, 'Invalid action.')
            return redirect('connection_requests')

        if connection.status != 'pending':
            messages.error(request, 'Connection request is not pending.')
            return redirect('connection_requests')

        connection.status = 'accepted' if action == 'accept' else 'declined'
        connection.save()
        messages.success(request, f'Connection request has been {connection.status}.')
        return redirect('connection_requests')


# Reference Letters
class ReferenceLetterCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = ReferenceLetterForm()
        return render(request, 'follows/reference_letter_form.html', {'form': form})

    def post(self, request):
        form = ReferenceLetterForm(request.POST)
        if form.is_valid():
            reference_letter = form.save(commit=False)
            reference_letter.author = request.user
            reference_letter.save()
            messages.success(request, 'Reference letter created successfully.')
            return redirect('reference_letters_list')
        return render(request, 'follows/reference_letter_form.html', {'form': form})


# List Reference Letters
class ReferenceLetterListView(LoginRequiredMixin, View):
    def get(self, request):
        reference_letters = ReferenceLetter.objects.filter(recipient=request.user)
        return render(request, 'follows/reference_letters_list.html', {'reference_letters': reference_letters})


# Request Reference
class RequestReferenceView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        recipient = get_object_or_404(CustomUser, id=user_id)
        is_followed = Follow.objects.filter(follower=request.user, followee=recipient).exists()
        is_connected = Connection.objects.filter(sender=request.user, receiver=recipient, status='accepted').exists() or \
                       Connection.objects.filter(sender=recipient, receiver=request.user, status='accepted').exists()

        if not (is_followed and is_connected):
            messages.error(request, 'You can only request a reference from friends (mutual follow and connection).')
            return redirect('reference_requests_list')

        form = ReferenceLetterForm()
        return render(request, 'follows/request_reference.html', {'form': form, 'recipient': recipient})

    def post(self, request, user_id):
        recipient = get_object_or_404(CustomUser, id=user_id)
        if recipient == request.user:
            messages.error(request, 'You cannot request a reference from yourself.')
            return redirect('reference_requests_list')

        is_followed = Follow.objects.filter(follower=request.user, followee=recipient).exists()
        is_connected = Connection.objects.filter(sender=request.user, receiver=recipient, status='accepted').exists() or \
                       Connection.objects.filter(sender=recipient, receiver=request.user, status='accepted').exists()

        if not (is_followed and is_connected):
            messages.error(request, 'You can only request a reference from friends (mutual follow and connection).')
            return redirect('reference_requests_list')

        form = ReferenceLetterForm(request.POST)
        if form.is_valid():
            reference_letter = form.save(commit=False)
            reference_letter.author = request.user
            reference_letter.recipient = recipient
            reference_letter.status = 'pending'
            reference_letter.save()
            messages.success(request, f'Reference request sent to {recipient.username}.')
            return redirect('reference_requests_list')
        return render(request, 'follows/request_reference.html', {'form': form, 'recipient': recipient})


# Manage Reference Requests
class ManageReferenceRequestView(LoginRequiredMixin, View):
    def post(self, request, reference_id, action):
        reference = get_object_or_404(ReferenceLetter, id=reference_id, recipient=request.user)
        if action not in ['accept', 'reject']:
            messages.error(request, 'Invalid action.')
            return redirect('reference_requests_list')

        if reference.status != 'pending':
            messages.error(request, 'Reference request is not pending.')
            return redirect('reference_requests_list')

        reference.status = 'accepted' if action == 'accept' else 'rejected'
        reference.save()
        messages.success(request, f'Reference request has been {reference.status}.')
        return redirect('reference_requests_list')
