from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView,CreateView, ListView,DetailView,UpdateView, DeleteView
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse_lazy
from social_app.forms import UserForm, UserProfileForm, NewPostForm , ReplyForm
from django.shortcuts import render
from social_app.models import AuthUser, Post,Userprofile , Reply,Texlike
from django.contrib.auth.forms import UserCreationForm
import re
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


def home(request):
   post_list = Post.objects.filter(date__lte=timezone.now()).order_by('-date')
   page = request.GET.get('page', 1)
   paginator = Paginator(post_list,1)
   try:
       posts = paginator.page(page)
   except PageNotAnInteger:
       posts = paginator.page(1)
   except EmptyPage:
       posts = paginator.page(paginator.num_pages)
   return render(request, 'social_app/post_list.html', {'posts': posts})

def getimages(request):
    photos = Post.objects.exclude(photo='').order_by('-date')
    print(photos)
    return render(request,'social_app/photos.html',{'photos':photos})

def getvideos(request):
    videos = Post.objects.filter(~Q(video__isnull=True)).order_by('-date')
    return render(request,'social_app/videos.html', {'videos':videos})


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
         b = Userprofile.objects.get(userid=request.user.id)
         if "youtube.com" in input_value:
             url_id = get_youtube_urls(input_value)
             print(url_id)
             text.video = url_id
         else:
             text.text = input_value
         text.photo = pic_value
         text.userid = a
         text.profileid = b
         text.expand = False
         text.date = timezone.now()
         text.likecount = 0

         if 'photo' in request.FILES:
             text.photo = request.FILES['photo']
             print(text.photo)

         text.save()

         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

########################################################################################################
########################################################################################################

def searchListView(request):
  """
  Display a List page filtered by the search query.
  """
  paginate_by = 10
  search_value = request.GET['q']

  if '@' in search_value:
      result_objects = User.objects.filter(email__icontains=search_value)
  else:
      result_objects = User.objects.filter(username__icontains=search_value)

  if result_objects:
       result_profilepic = Userprofile.objects.filter(userid=result_objects[0].id)
       context = {
           'result_objects': result_objects,
           'result_profilepic': result_profilepic
       }
       return render(request,'social_app/search_result.html',context)
  else:
       messages.info(request, 'No results found, please try again')
       return render(request,'social_app/search_result.html')

def signup_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    user_form = UserForm()
    user_img = UserProfileForm()
    if request.method == 'POST' and request.POST.get('submit') == 'login':
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
           return render(request,'registration/login.html',{'user_form':user_form, 'user_img':user_img})

    elif request.method == 'POST' and request.POST.get('submit') == 'signup':
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
           profile.portfolio = ''
           profile.bio = ''
           profile.status = False
           profile.postcount = 0
           profile.followercount = 0
           profile.followingcount = 0
           if 'profilepic' in request.FILES:
               profile.profilepic= request.FILES['profilepic']
           elif not 'profilepic' in request.FILES and profile.gender == 'M':
               profile.profilepic = 'profile_pics/male-default-pic-big.jpg'
           elif not 'profilepic' in request.FILES and profile.gender == 'F':
               profile.profilepic = 'profile_pics/avatar-female.png'
           profile.save()
           registered = True
           return HttpResponseRedirect(reverse('signup_login'))
       else:
           print (user_form.errors)
           print (user_img.errors)
    else:
       registered = False
       user_form = UserForm()
       user_img = UserProfileForm()
       return render(request,'registration/login.html',{'user_form':user_form,'registered':registered, 'user_img':user_img})
    return render(request,'registration/login.html',{'user_form':user_form, 'user_img':user_img})


def post_reply(request,pk):
    #post_id = get_object_or_404(Post,pk=pk)
    if request.method == "POST":
       text_form = ReplyForm(data=request.POST)
       if text_form.is_valid():
           reply_content = request.POST.get('reply')
           text_form.save(commit=False)
           text_form.instance.date = timezone.now()
           text_form.instance.userid = AuthUser.objects.get(id=request.user.id)
           text_form.instance.profileid = Userprofile.objects.get(userid=request.user.id)
           text_form.instance.textid = Post.objects.get(id=pk)
           print(text_form.instance.textid.id)
           text_form.reply = reply_content
           text_form.instance.likecount = 0
           text_form.save()
       return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
       return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

######################################## UPDATING USER ################################################
class UserUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'auth/user_form.html'
    form_class = UserForm
    model = User


def userupdate(request):
     updated = False
     user_profile = Userprofile.objects.get(userid=request.user.id)
     if request.method == 'POST':
         user_img = UserProfileForm(data=request.POST,instance=user_profile)
         port_value = request.POST.get('portfolio')
         bio_value = request.POST.get('bio')
         if user_img.is_valid():
             a = AuthUser.objects.get(id=request.user.id)
             profile = user_img.save(commit=False)
             profile.userid = a
             profile.portfolio = port_value
             profile.bio = bio_value
             profile.status = False
             profile.postcount = 0
             profile.followercount = 0
             profile.followingcount = 0

             if 'profilepic' in request.FILES:
                 profile.profilepic= request.FILES['profilepic']
                 print(profile.profilepic)


             profile.save()
             updated = True

         else:
             print(user_img.errors)

     else:
        user_img = UserProfileForm()

     return render(request,'auth/user_form.html',{'user_img':user_img})





def likepost(request,pk):

    if Texlike.objects.filter(userid=AuthUser.objects.get(id=request.user.id),textid=Post.objects.get(id=pk)).exists():
        like = Texlike.objects.filter(userid=AuthUser.objects.get(id=request.user.id),textid=Post.objects.get(id=pk))

        print(like)
        like.delete()
    else:
        like = Texlike()
        a = AuthUser.objects.get(id=request.user.id)
        d = Post.objects.get(id=pk)
        like.userid = a
        like.textid = d
        d.likecount+= 1
        like.save()
        d.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
