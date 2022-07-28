from django.shortcuts import render
from django.urls import reverse 
from django.http import HttpResponseRedirect
# Create your views here.

def index(request):
    context = {
        "page_name" : "Index"
    }
    return render(request,'index.html',context)
