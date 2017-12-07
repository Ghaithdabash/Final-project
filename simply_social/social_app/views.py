from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView,CreateView, ListView,DetailView,UpdateView, DeleteView
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse_lazy
from social_app.forms import UserForm, UserProfileForm, NewPostForm , ReplyForm
from django.shortcuts import render
from social_app.models import AuthUser, Post, Userprofile , Reply, Texlike, Follower, Following, Replylike
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
import collections

# Create your views here.


def home(request):
   post_list = Post.objects.filter(date__lte=timezone.now()).order_by('-date')
   arr_of_like_objs = {}
   for post in post_list:
       check = Texlike.objects.filter(userid=AuthUser.objects.get(id=request.user.id),textid=Post.objects.get(id=post.id))
       if check.exists():
           arr_of_like_objs[post] = check

   page = request.GET.get('page', 1)
   paginator = Paginator(post_list,10)
   try:
       posts = paginator.page(page)
   except PageNotAnInteger:
       posts = paginator.page(1)
   except EmptyPage:
       posts = paginator.page(paginator.num_pages)

   try:
       followers = Follower.objects.get(followerid=request.user.id)
   except:
       return render(request, 'social_app/post_list.html', {'posts': posts,'arr_of_like_objs':arr_of_like_objs})

   return render(request, 'social_app/post_list.html', {'posts': posts,'arr_of_like_objs':arr_of_like_objs,'followers':followers})

def getimages(request):
    photos = Post.objects.exclude(photo='').order_by('-date')
    arr_of_like_objs = {}
    for post in photos:
        check = Texlike.objects.filter(userid=AuthUser.objects.get(id=request.user.id),textid=Post.objects.get(id=post.id))
        if check.exists():
            arr_of_like_objs[post] = check

    return render(request,'social_app/photos.html',{'photos':photos,'arr_of_like_objs':arr_of_like_objs})

def getvideos(request):
    videos = Post.objects.filter(~Q(video__isnull=True)).order_by('-date')
    arr_of_like_objs = {}
    for post in videos:
        check = Texlike.objects.filter(userid=AuthUser.objects.get(id=request.user.id),textid=Post.objects.get(id=post.id))
        if check.exists():
            arr_of_like_objs[post] = check

    return render(request,'social_app/videos.html', {'videos':videos,'arr_of_like_objs':arr_of_like_objs})

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
         b.postcount += 1
         b.save()

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
 result_profilepic ={}
 result_follower = {}
 current_user = AuthUser.objects.get(id=request.user.id)
 if result_objects:
     for result in result_objects:
          result_profilepic[result] = Userprofile.objects.filter(userid=result.id)
          follower = Follower.objects.filter(followerid=current_user.id,userid=result.id)
          print(current_user.id)
          print(result.id)
          print(follower)
          for followers in follower:
              if followers.followerid == current_user.id:
                  result_follower[followers.id] = followers
                  print(result_follower)
     context = {
              'result_objects': result_objects,
              'result_profilepic': result_profilepic,
              'result_follower':result_follower,
              'current_user':current_user,
          }
     return render(request,'social_app/search_result.html',context)
 else:
      messages.info(request, 'No results found, please try again')
      return render(request,'social_app/search_result.html')

def get_user_profile(request,pk):
  var = pk
  user1 = AuthUser.objects.get(id=request.user.id)
  profile_info = AuthUser.objects.get(id=var)

  my_post = Post.objects.filter(userid=var)
  all_post={}

  for post in my_post:
        all_post[post.id]= post

  follower = Follower.objects.filter(followerid=user1.id,userid=var)
  for followers in follower:
      if followers.followerid == user1.id:
          follower = followers
  profile_pic = Userprofile.objects.get(userid=var)
  return render(request, 'social_app/profile_search.html', {'user': profile_info ,'profile_pic': profile_pic,
                                              'follower':follower,'user1':user1,'all_post':all_post})

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
    def get_success_url(self):
        return '/'

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

def update_status(request):
   c_user = AuthUser.objects.get(id=request.user.id)
   c_userprofile = Userprofile.objects.get(userid=c_user.id)
   print(request.POST.get('status'))
   if request.method == 'POST' and request.POST.get('status'):
       print(request.POST.get('status'))
       c_userprofile.status = 'f'
   else:
       c_userprofile.status = 't'
   c_userprofile.save()
   return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def follow_request(request,pk):
    user1 = AuthUser.objects.get(id=request.user.id)
    print(user1.id)
    user = Userprofile.objects.get(userid=user1)
    print(user.id)

    user2 = Userprofile.objects.get(userid=pk)
    print(user2.userid.id)
    follower = Follower()
    following = Following()

    if user2.status == False:
        following.followingid = user2.id
        following.userid = user1
        following.save()
        user.followingcount += 1
        user.save()
        ########################
        follower.followerid = user1.id

        follower.userid = AuthUser(user2.userid.id)
        follower.connected = True
        follower.save()
        user2.followercount +=1
        user2.save()

    else:
        follower.followerid = user1.id
        follower.userid = AuthUser(user2.userid.id)
        follower.connected = False
        follower.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def approve_request(request,pk):
    user1 = AuthUser.objects.get(id=request.user.id)
    user = Userprofile.objects.get(userid=user1)

    user2 = Userprofile.objects.get(userid=pk)
    follower = Follower.objects.get(userid=user1,followerid=user2.userid.id)


    follower.connected = 't'
    follower.save()
    user.followercount += 1
    user2.followingcount +=1
    user.save()
    user2.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def current_requests(request):
    current_user = AuthUser.objects.get(id=request.user.id)
    f_req = Follower.objects.filter(connected='f',userid=current_user)

    all_req={}
    follower_p = {}
    follower_profile = {}
    for req in f_req:
       all_req[req.id]= req
       follower_p[req.id] = Userprofile.objects.filter(userid=req.followerid)
       print(follower_p)
       for key,follower in follower_p.items():
         print(follower)
         for value in follower:
             if value.userid.id == req.followerid:
                 follower_profile[value.id] = value

    print(follower_profile)
    return render(request,'social_app/following_requests.html',{'all_req':all_req,'follower_profile':follower_profile})

def deny_request(request,pk):

    user1 = AuthUser.objects.get(id=request.user.id)
    follower = Follower()
    ########################
    follower = Follower.objects.filter(followerid=pk,userid=user1.id)
    follower.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def Unfollow_request(request,pk):

    user1 = AuthUser.objects.get(id=request.user.id)
    user = Userprofile.objects.get(userid=user1.id)
    user2 = Userprofile.objects.get(userid=pk)
    follower = Follower()
    following = Following()

    following = Following.objects.filter(followingid=user2.id,userid=user1)

    following.delete()
    user.followingcount -= 1
    user.save()
    ########################
    follower = Follower.objects.filter(followerid=user1.id,userid=AuthUser(user2.userid.id))

    follower.delete()
    user2.followercount -=1
    user2.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def follower_list(request):
   current_user = AuthUser.objects.get(id=request.user.id)
   profile_result={}
   user_list = {}
   following_list = Follower.objects.filter(userid = current_user.id)
   print(following_list)

   for following in following_list :
       print(following.userid.id)
       profile_following = Userprofile.objects.filter(userid = following.followerid)
       user_following = AuthUser.objects.filter(id=following.followerid)

       for profile in profile_following:
           profile_result[following] = profile
           print(profile.id)

       for user in user_following:
           user_list[following] = user
           print(user.username)

   return render(request,'social_app/Followers.html',{'following_list':following_list,'profile_result':profile_result,
                                                                   'user_list':user_list,})

def following_list(request):
       current_user = AuthUser.objects.get(id=request.user.id)
       profile_result={}
       user_list = {}

       following_list = Follower.objects.filter(followerid=current_user.id)

       for following in following_list :
           profile_following = Userprofile.objects.filter(userid=following.userid.id)
           user_following = AuthUser.objects.filter(id=following.userid.id)

           for profile in profile_following:
               profile_result[following.userid.id] = profile

           for user in user_following:
               user_list[following.userid.id] = user

       return render(request,'social_app/Following.html',{'following_list':following_list,'profile_result':profile_result,
                                                           'user_list':user_list,})

def likepost(request,pk):
    a = AuthUser.objects.get(id=request.user.id)
    d = Post.objects.get(id=pk)
    if Texlike.objects.filter(userid=AuthUser.objects.get(id=request.user.id),textid=Post.objects.get(id=pk)).exists():
        like = Texlike.objects.filter(userid=AuthUser.objects.get(id=request.user.id),textid=Post.objects.get(id=pk))
        d.likecount-= 1
        d.save()
        like.delete()
    else:
        like = Texlike()
        like.userid = a
        like.textid = d
        d.likecount+= 1
        like.save()
        d.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def likecomment(request,pk):
    a = AuthUser.objects.get(id=request.user.id)
    d = Reply.objects.get(id=pk)
    if Replylike.objects.filter(userid=a,replyid=d).exists():
        like = Replylike.objects.filter(userid=AuthUser.objects.get(id=request.user.id),replyid=Post.objects.get(id=pk))
        d.likecount-= 1
        d.save()
        like.delete()
    else:
        like = Replylike()
        like.userid = a
        like.replyid = d
        d.likecount+= 1
        like.save()
        d.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def profile_post(request):
    current_user = AuthUser.objects.get(id=request.user.id)
    my_post = Post.objects.filter(userid=current_user.id)
    all_post={}

    for post in my_post:
       all_post[post.id]= post


    my_likes = Texlike.objects.filter(userid=current_user)
    my_liked_post={}
    total_liked_post={}
    row=0
    for postlike in my_likes:
     my_liked_post[postlike.textid.id]= Post.objects.filter(id=postlike.textid.id)
     total_liked_post[postlike.textid.id]=my_liked_post[postlike.textid.id][row]

    my_reply = Reply.objects.filter(userid=current_user)
    print(my_reply)
    my_reply_post={}
    total_reply_post={}
    row=0
    for reply in my_reply:
     print(reply.textid.id)
     my_reply_post[reply.textid.id]= Post.objects.filter(id=reply.textid.id)
     total_reply_post[reply.textid.id]=my_reply_post[reply.textid.id][row]
     print(total_reply_post[reply.textid.id].id)

    all_post.update(total_liked_post)
    all_post.update(total_reply_post)

    all_posts = collections.OrderedDict(sorted(all_post.items()),)

    return render(request,'social_app/profile.html',{'all_posts':all_posts})

def my_likes(request):
 current_user = AuthUser.objects.get(id=request.user.id)
 all_post={}


 my_likes = Texlike.objects.filter(userid=current_user)
 my_liked_post={}
 total_liked_post={}
 row=0
 for postlike in my_likes:
     my_liked_post[postlike.textid.id]= Post.objects.filter(id=postlike.textid.id)
     total_liked_post[postlike.textid.id]=my_liked_post[postlike.textid.id][row]


 all_post.update(total_liked_post)
 all_posts = collections.OrderedDict(sorted(all_post.items()),)

 #for i ,post in enumerate(my_liked_post):
  #       print (i,post,my_liked_post[post][i])
 return render(request,'social_app/my_likes.html',{'all_posts':all_posts})




def my_reply(request):
 current_user = AuthUser.objects.get(id=request.user.id)
 all_post={}

 my_reply = Reply.objects.filter(userid=current_user)
 print(my_reply)
 my_reply_post={}
 total_reply_post={}
 row=0
 for reply in my_reply:
     print(reply.textid.id)
     my_reply_post[reply.textid.id]= Post.objects.filter(id=reply.textid.id)
     total_reply_post[reply.textid.id]=my_reply_post[reply.textid.id][row]
     print(total_reply_post[reply.textid.id].id)


 all_post.update(total_reply_post)
 all_posts = collections.OrderedDict(sorted(all_post.items()),)

 #for i ,post in enumerate(my_liked_post):
  #       print (i,post,my_liked_post[post][i])
 return render(request,'social_app/my_reply.html',{'all_posts':all_posts})
