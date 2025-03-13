from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from users.forms import RegisterForm, CustomRegisterForm
from django.contrib.auth import logout, authenticate, login

def Signup(request):
    if request.method == "GET":
        form = CustomRegisterForm()
    if request.method == "POST":
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    
    return render(request, "register.html", {'form': form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            print(f'✅ User {user} login success')
            login(request, user)
            return redirect('home')

    return render(request, "login.html")

def logout_view(request):
        logout(request)
        return redirect('login')