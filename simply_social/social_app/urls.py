from django.conf.urls import url
from social_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

        url(r'^$',views.signup_login,name='signup_login'),
        url(r'^fvzdfgjx35113s3sf51ahFGLdhome/$',views.PostListView.as_view(),name='home'),
        url(r'search/$',views.SearchListView.as_view(), name='search_list_view'),
        url(r'^add/post/$',views.newpost,name='new_post'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
