from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.conf import settings
from django.template import RequestContext, Context
from authentication.models import *
from core.models import *
from authentication.forms import *
from pyfb import Pyfb
import datetime, random, tweepy, shlex


def feed(request):
	usergenres = request.user.genretouser.all()
	var = RequestContext(request, {
        'user':request.user,
        'genres':usergenres
        })
	return render_to_response('pages/feed.html', var)