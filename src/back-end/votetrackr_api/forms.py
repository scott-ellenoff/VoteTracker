from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Vote

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'email', 'district',)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'district',)

class CustomVoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ('bill', 'legislator', 'user', 'vote')

    def clean(self):
        cleaned_data = super(CustomVoteForm, self).clean()
        legislator = cleaned_data.get('legislator')
        user = cleaned_data.get('user'),

        if user and legislator or not user and not legislator:
            raise forms.ValidationError('Exactly one of User and Legislator must be set')

        return cleaned_data