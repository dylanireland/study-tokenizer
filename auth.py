from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .forms import AuthForm



def auth(request):

    return HttpResponse(loader.get_template('studytokenizer/auth.html').render({"form": AuthForm()}, request))
