from django.template import RequestContext
from social_app.models import AuthUser, Userprofile
from django.contrib.auth import login, logout, authenticate


def get_profile(request):
    if request.user.is_authenticated():
        user = AuthUser.objects.get(id=request.user.id)
        profile = Userprofile.objects.get(userid=user)
        return {'user': request.user,'profile':profile}
    else:
        return {'user': request.user}
