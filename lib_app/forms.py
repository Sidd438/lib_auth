from allauth.account.forms import SignupForm
from django import forms


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    bits_id = forms.CharField(max_length=20, label='BITS ID', required=False)
    hostel = forms.CharField(max_length=20, required=False)
    room_no = forms.IntegerField(required=False)
    phone_number = forms.CharField(max_length=12, required=False)

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.bits_id = self.cleaned_data['bits_id']
        user.save()
        user.profile.bits_id = self.cleaned_data['bits_id']
        user.profile.hostel = self.cleaned_data['hostel']
        user.profile.room_no = self.cleaned_data['room_no']
        user.profile.phone_number = self.cleaned_data['phone_number']
        user.save()
        return user