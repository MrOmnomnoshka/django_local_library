from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime  # for checking renewal date range.

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation


class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password', strip=False, help_text=password_validation.password_validators_help_text_html(),
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'form-control',
            'placeholder': 'Create password'}))
    password2 = forms.CharField(
        label='Repeat password', strip=False, help_text="Enter the same password as before, for verification.",
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'form-control',
            'placeholder': 'Repeat password'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email',)
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email address'
            })
        }

    # def clean_password2(self):
    #     print("clean psw?")
    #     cd = self.cleaned_data
    #     print(cd)
    #     if cd['password1'] != cd['password2']:
    #         raise forms.ValidationError('Passwords don\'t match.')
    #     print(cd['password2'])
    #     return cd['password2']


class RenewBookForm(forms.Form):
    """Form for a librarian to renew books."""
    renewal_date = forms.DateField(
        help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # Check date is not in past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))
        # Check date is in range librarian allowed to change (+4 weeks)
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(
                _('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data
