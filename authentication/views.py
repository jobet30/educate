from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
from .forms import (
    UserRegistrationForm,
    UserPasswordChangeForm,
    UserProfileUpdateForm
)


class UserRegistrationView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            send_mail(
                'Welcome to Our Site!',
                'Thank you for registering. Please confirm your email address.',
                'from@example.com',
                [user.email],
                fail_silently=False,
            )
            messages.success(
                request, 'Registration successful. Welcome! Please check your email to confirm.')
            return redirect('login')
        messages.error(
            request, 'Registration failed. Please correct the errors below.')
        return render(request, 'registration/register.html', {'form': form})


class PasswordChangeView(View):
    def get(self, request):
        form = UserPasswordChangeForm(user=request.user)
        return render(request, 'registration/password_change.html', {'form': form})

    def post(self, request):
        form = UserPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully.')
            return redirect('profile')
        messages.error(request, 'Please correct the errors below.')
        return render(request, 'registration/password_change.html', {'form': form})


class UserProfileUpdateView(View):
    def get(self, request):
        form = UserProfileUpdateForm(instance=request.user)
        return render(request, 'registration/profile_update.html', {'form': form})

    def post(self, request):
        form = UserProfileUpdateForm(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
        messages.error(request, 'Please correct the errors below.')
        return render(request, 'registration/profile_update.html', {'form': form})
