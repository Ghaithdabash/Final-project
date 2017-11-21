from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView,CreateView, ListView,DetailView,UpdateView, DeleteView
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
# Create your views here.

class Home(TemplateView,LoginRequiredMixin):
    template_name = 'registration/login.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect('https://www.google.com')
        return super(Home, self).dispatch(request, *args, **kwargs)
