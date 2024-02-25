from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import gettext,gettext_lazy as _
from django.contrib.auth import password_validation
from .models import Customer
from .models import Contact
# from .models import Product


class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', 
                                widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password', 
                                widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.CharField(required=True, 
                                widget=forms.EmailInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        labels = {'email': 'Email'}
        widgets = {'username': forms.TextInput(attrs={'class':'form-control'})}


    def clean_email(self):
        data = self.cleaned_data['email']
        domain = data.split('@')[1]
        domain_list = ["gmail.com", "yahoo.com", "hotmail.com",]
        if domain not in domain_list:
            raise forms.ValidationError("Please enter an Email Address with a valid domain")
        return data
    
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs=
                                                    {'autofocus':True,'class':'form-control'}))
    password = forms.CharField(label=_("Password"),
                               strip=False,
                               widget=forms.PasswordInput(attrs=
                                                    {'autocomplete':'current-password','class':'form-control'}))
    
class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("Old Password"),strip=False,widget=forms.PasswordInput(attrs=
                                                                                                  {'autocomplete': 'current-password','autofocus':True,'class':'form-control'}))
    new_password1 = forms.CharField(label=_("New Password"),strip=False,widget=forms.PasswordInput(attrs=
                                                                           {'autocomplete':'new-password','class':'form-control'}),
                                                                            help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm New Password"),strip=False,widget=forms.PasswordInput(attrs=
                                                                           {'autocomplete':'new-password','class':'form-control'}))
    
class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=("Email"),max_length=254, widget=forms.EmailInput(attrs={'autocomplete':'email',
    'class':'form-control'}))

class MySetPasswordForm(SetPasswordForm):
     new_password1 = forms.CharField(label=_("New Password"),
                                    strip=False,widget=forms.PasswordInput(attrs=
                                                                           {'autocomplete':'new-password',
                                                                            'class':'form-control'}),
    help_text=password_validation.password_validators_help_text_html())
     new_password2 = forms.CharField(label=_("Confirm New Password"),
                                    strip=False,widget=forms.PasswordInput(attrs=
                                                                           {'autocomplete':'new-password','class':'form-control'}))
     
class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name','locality','city','state','zipcode']
        widgets = {'name':forms.TextInput(attrs={'class':'form-control'}),
                   'locality':forms.TextInput(attrs={'class':'form-control'}),
                   'city':forms.TextInput(attrs={'class':'form-control'}),
                   'state':forms.Select(attrs={'class':'form-control'}),
                   'zipcode':forms.NumberInput(attrs={'class':'form-control'})}
        

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
        
