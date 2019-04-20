from django import forms

class UserForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    password = forms.CharField(label="Password", max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)
    email = forms.CharField(label="Email", max_length=50, widget=forms.EmailInput(attrs={'class': 'form-control'}), required=True)
    phoneNumber = forms.CharField(label="Phone number", max_length=20, widget=forms.NumberInput(attrs={'class': 'form-control'}), required=True)
    notify_email = forms.BooleanField()
    notify_sms = forms.BooleanField()
