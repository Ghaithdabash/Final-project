from django.template import RequestContext
from social_app.forms import UserForm, UserProfileForm
from django.shortcuts import render
from social_app.models import AuthUser
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
