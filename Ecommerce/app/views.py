from django.shortcuts import render,redirect,HttpResponse

def home(request):
    return HttpResponse("This is working !!!!")
def test(request):
    return HttpResponse("This is working !!!!")