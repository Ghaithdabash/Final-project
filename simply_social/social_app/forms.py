from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from social_app.models import Userprofile
#from django.db import models




class UserProfileForm(forms.ModelForm):
    CHOICES = (('M', 'Male',), ('F', 'Female',))
    gender = forms.TypedChoiceField(
                choices=CHOICES, widget=forms.RadioSelect()
                )
    class Meta():
        model = Userprofile
        fields = ('profilepic','gender',)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['gender'].label = 'Gender'
        self.fields['profilepic'].label = 'Profile Picture'

class UserForm(UserCreationForm):

  class Meta():
       model = User
       fields = ('username','first_name','last_name','email','password1','password2',)

  def save(self,commit=True):
      user = super(UserForm,self).save(commit=False)
      user.username = self.cleaned_data["username"]
      user.email = self.cleaned_data["email"]
      user.first_name = self.cleaned_data["first_name"]
      user.last_name = self.cleaned_data["last_name"]
      user.password1 = self.cleaned_data["password1"]
      user.password2 = self.cleaned_data["password2"]
      if commit:
          user.save()
      return user


  def __init__(self,*args,**kwargs):
       super().__init__(*args,**kwargs)
       self.fields['username'].label = 'Username'
       self.fields['first_name'].label = 'First Name'
       self.fields['last_name'].label = 'Last Name'
       self.fields['email'].label = 'Email Address'
       self.fields['password1'].label = 'Password'
       self.fields['password2'].label = 'Re-enter Password'
