from django.shortcuts import render,redirect,HttpResponse
<<<<<<< HEAD

def home(request):
    return render(request,"index.html")

=======

def home(request):
    return HttpResponse("Hello This is working !!!!")
>>>>>>> b718097fcec6015f05785010fc1a60ac98cc2e25
