from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

def index(request):
    return render(request, 'apItems/index.html')

def item(request, id):
	return render(request, 'apItems/item.html')