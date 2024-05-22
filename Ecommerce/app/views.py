from django.shortcuts import render,redirect,HttpResponse

def home(request):
    return HttpResponse("Hello This is working !!!!")