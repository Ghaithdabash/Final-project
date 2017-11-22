from django.conf.urls import url
from social_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
        url(r'^$',views.Reg.as_view(),name='reg'),
        url(r'^login/$',views.user_login,name='login'),
        url(r'^register/$',views.register,name='register'),
        url(r'^home/$',views.Home.as_view(),name='home'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
