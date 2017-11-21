from django.template import RequestContext
from social_app.forms import UserForm, UserProfileForm
from django.shortcuts import render
from social_app.models import AuthUser

def register(request):
     registered = False

     if request.method == 'POST':
         user_form = UserForm(data=request.POST)
         user_img = UserProfileForm(data=request.POST)

         if user_form.is_valid() and user_img.is_valid():
             user = user_form.save()
             user.set_password(user.password1)

             user.save()

             a = AuthUser.objects.get(id=user.id)
             profile = user_img.save(commit=False)
             profile.userid = a

             if 'profilepic' in request.FILES:
                 profile.profilepic= request.FILES['profilepic']
                 print(profile.img)


             profile.save()
             registered = True

         else:
             print(user_form.errors,user_img.errors)

     else:
        user_form = UserForm()
        user_img = UserProfileForm()

     return {'user_form':user_form,'registered':registered, 'user_img':user_img}
