from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from .models import CustomUser


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=True, label='First Name')
    last_name = forms.CharField(
        max_length=30, required=True, label='Last Name')
    email = forms.EmailField(required=True, label='Email Address')
    date_of_birth = forms.DateField(
        required=True, label='Date of Birth', widget=forms.SelectDateWidget(years=range(1900, 2100)))
    gender_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = forms.ChoiceField(
        choices=gender_choices, required=True, label='Gender')
    profile_picture = forms.ImageField(required=False, label='Profile Picture')

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email',
                  'password1', 'password2', 'date_of_birth', 'gender', 'profile_picture')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("This email address is already in use.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username.isalnum():
            raise ValidationError("Username must be alphanumeric.")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("The two password fields didn't match.")
        return password2


class UserProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Email Address')
    date_of_birth = forms.DateField(
        required=True, label='Date of Birth', widget=forms.SelectDateWidget(years=range(1900, 2100)))
    gender_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = forms.ChoiceField(
        choices=gender_choices, required=True, label='Gender')

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email',
                  'date_of_birth', 'gender', 'profile_picture')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise ValidationError("This email address is already in use.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username.isalnum():
            raise ValidationError("Username must be alphanumeric.")
        return username


class UserPasswordChangeForm(PasswordChangeForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput, label='New Password', min_length=8)
    new_password2 = forms.CharField(
        widget=forms.PasswordInput, label='Confirm New Password')

    class Meta:
        model = CustomUser
        fields = ('old_password', 'new_password1', 'new_password2')

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("The two password fields must match.")
        if password1.isnumeric() or password1.isalpha():
            raise ValidationError(
                "Password must contain both letters and numbers.")
        return password2

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise ValidationError("Old password is incorrect.")
        return old_password
