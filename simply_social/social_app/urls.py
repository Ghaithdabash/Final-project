from django.conf.urls import url
from social_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
        url(r'^$',views.Home.as_view(),name='login'),
    #    url(r'^register/$',views.register,name='register'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
