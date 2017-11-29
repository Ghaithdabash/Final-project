from django.conf.urls import url,include
from social_app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [

        url(r'^$',views.signup_login,name='signup_login'),
        url(r'^fvzdfgjx35113s3sf51ahFGLdhome/$',views.PostListView.as_view(),name='home'),
        url(r'^add/post/$',views.newpost,name='new_post'),
        url(r'^photos/$',views.getimages,name='photos'),
        url(r'^videos/$',views.getvideos,name='videos'),
        url(r'^login/$', auth_views.login, name='login'),
        url(r'^logout/$', auth_views.logout, name='logout'),
        url(r'^oauth/', include('social_django.urls', namespace='social')),
        url(r'^reply/(?P<pk>\d+)/$',views.post_reply,name='post_reply'),
        url(r'^search/$',views.searchListView, name='search_list_view'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
