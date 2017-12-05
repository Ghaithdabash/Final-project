from django.conf.urls import url,include
from social_app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [

        url(r'^$',views.signup_login,name='signup_login'),
        url(r'^home/$',views.home,name='home'),
        url(r'^add/post/$',views.newpost,name='new_post'),
        url(r'^photos/$',views.getimages,name='photos'),
        url(r'^videos/$',views.getvideos,name='videos'),
        url(r'^login/$', auth_views.login, name='login'),
        url(r'^logout/$', auth_views.logout, name='logout'),
        url(r'^oauth/', include('social_django.urls', namespace='social')),
        url(r'^reply/(?P<pk>\d+)/$',views.post_reply,name='post_reply'),
        url(r'^search/$',views.searchListView, name='search_list_view'),
        url(r'^user/profile/update/(?P<pk>\d+)/$',views.UserUpdateView.as_view(),name='user_update'),
        url(r'^user/profile/update/$',views.userupdate,name='user_update2'),
        url(r'^post/(?P<pk>\d+)/like/$',views.likepost,name='like'),
        url(r'^get_user_profile/(?P<pk>\d+)$',views.get_user_profile,name='get_user_profile'),
        url(r'^follow_request/(?P<pk>\d+)$',views.follow_request,name='follow_request'),
        url(r'^Unfollow_request/(?P<pk>\d+)$',views.Unfollow_request,name='unfollow_request'),
        url(r'^followers/$',views.follower_list,name='follower'),
        url(r'^following/$',views.following_list,name='following'),
        url(r'^profile/$',views.profile_post,name='profile'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
