from django import forms
from userProfile.models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address']  # Specify the fields you want to include in the form
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user object from kwargs if passed
        super().__init__(*args, **kwargs)
        if user:
            self.fields['phone_number'].disabled = True if user.profile.phone_number else False
            self.fields['address'].disabled = True if user.profile.address else False
