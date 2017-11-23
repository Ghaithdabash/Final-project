from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView,CreateView, ListView,DetailView,UpdateView, DeleteView
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse_lazy
from social_app.forms import UserForm, UserProfileForm
from django.shortcuts import render
from social_app.models import AuthUser
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
# Create your views here.


class Reg(TemplateView):
    template_name = 'registration/login.html'


class Home(TemplateView):
    template_name = 'social_app/home.html'
    #def dispatch(self, request, *args, **kwargs):
    #    if request.user.is_authenticated():
    #        return HttpResponseRedirect('https://www.google.com')
    #    return super(Home, self).dispatch(request, *args, **kwargs)


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)



                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse("ACCOUNT IS NOT ACTIVE!")
        else:
            print("Some one is trying to login and failed")
            print("Username: {} and Password: {}".format(username,password))
            return HttpResponse("Invalid login details Supplied!")

    else:
        return render(request,'registration/login.html',{})

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
             profile.satus = False
             profile.postcount = 0
             profile.followercount = 0
             profile.followingcount = 0

             if 'profilepic' in request.FILES:
                 profile.profilepic= request.FILES['profilepic']

             profile.save()
             registered = True

         else:
             print(user_form.errors,user_img.errors)

     else:
        user_form = UserForm()
        user_img = UserProfileForm()

     return render(request,'registration/login.html',{'user_form':user_form,'registered':registered, 'user_img':user_img})
