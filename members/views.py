from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages



def login_user(request):
    if request.method== "POST":
        username= request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username= username, password= password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.success(request, ("Napaka pri logiranju..."))
            return redirect("login")
    
    else:
        return render(request, "registration/login.html",{})


def logout_user(request):
    logout(request)
    messages.success(request, ("Odjavil si se..."))
    return redirect("index")
