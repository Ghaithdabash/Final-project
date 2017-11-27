from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView,CreateView, ListView,DetailView,UpdateView, DeleteView
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse_lazy
from social_app.forms import UserForm, UserProfileForm, NewPostForm
from django.shortcuts import render
from social_app.models import AuthUser, Post
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
import re
# Create your views here.


class PostListView(ListView,LoginRequiredMixin):
   model = Post
   def get_queryset(self):
       return Post.objects.filter(date__lte=timezone.now()).order_by('-date')

#class CreateTextView(LoginRequiredMixin,CreateView):
#    login_url = '/login/'
#    redirect_field_name = 'social_app/text_list.html'
#    form_class = NewPostForm
#    model = Text

#    def form_valid(self, form):
#        a = AuthUser.objects.get(id=self.request.user.id)
#        form.instance.userid = a
#        form.instance.expand = False
#        form.instance.date = timezone.now()
#        form.instance.likecount = 0
#        return super(CreateTextView, self).form_valid(form)
def get_youtube_urls(inputv):

    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

    matches = re.findall(youtube_regex, inputv)


    for url in matches:
        y_id = url[-1]        # from last index of `matches` list.
        if len(y_id) == 11:   # check if `id` is valid or not.
            urls = y_id
    return urls

def newpost(request):

     if request.method == 'POST':
         text_form = NewPostForm(data=request.POST)
         input_value = request.POST.get('p')
         pic_value = request.POST.get('pic')

         text = text_form.save(commit=False)
         a = AuthUser.objects.get(id=request.user.id)
         if "youtube.com" in input_value:
             url_id = get_youtube_urls(input_value)
             print(url_id)
             text.video = url_id
         else:
             text.text = input_value
         text.photo = pic_value
         text.userid = a
         text.expand = False
         text.date = timezone.now()
         text.likecount = 0

         if 'photo' in request.FILES:
             text.photo = request.FILES['photo']
             print(text.photo)

         text.save()

         return HttpResponseRedirect(reverse('home'))


########################################################################################################
########################################################################################################
#class Home(TemplateView):
#    template_name = 'social_app/home.html'
    #def dispatch(self, request, *args, **kwargs):
    #    if request.user.is_authenticated():
    #        return HttpResponseRedirect('social_app/home.html')
    #    return super(Home, self).dispatch(request, *args, **kwargs)

class SearchListView(ListView):
   template_name = "base.html"
   """
   Display a List page filtered by the search query.
   """
   paginate_by = 10
   def get_queryset(self):

       search_value = self.request.GET['q']
       if "@" in search_value:
           result_objects = User.objects.filter(email__icontains=search_value)
           print(result_objects[0].username)
           return result_objects
       else:
           result_objects = User.objects.filter(username__icontains=search_value)
           print(result_objects[0].username)
           return result_objects
          # return result_objects

def signup_login(request):
     if request.method == 'POST':
         if request.POST.get('submit') == 'login':
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
                 return render(request,'registration/login.html',{})
         elif request.POST.get('submit') == 'signup':
             registered = False
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

                 if not 'profilepic' in request.FILES and profile.gender == 'M':
                    profile.profilepic = 'profile_pics/male-default-pic-big.jpg'

                 if not 'profilepic' in request.FILES and profile.gender == 'F':
                    profile.profilepic = 'profile_pics/avatar-female.png'
                 profile.save()
                 registered = True
                 return HttpResponseRedirect(reverse('signup_login'))
             else:
                 print(user_form.errors,user_img.errors)

         else:
            user_form = UserForm()
            user_img = UserProfileForm()
            return render(request,'registration/login.html',{'user_form':user_form,'registered':registered, 'user_img':user_img})
     else:
        user_form = UserForm()
        user_img = UserProfileForm()
        return render(request,'registration/login.html',{'user_form':user_form, 'user_img':user_img})
