from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.forms import CustomUserCreationForm

# Create your views here.

def loginPage(request):
    context = {}

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        UserModel = get_user_model()

        if username=='' and password=='':
            pass
        else:
            try:
                user = UserModel.objects.get(username=username) # 验证账号是否存在
            except:
                context = {'error':'User does not exist!'}
            else:
                user = authenticate(request,username=username,password=password)    # 验证账号和密码是否相符

                if user:
                    login(request,user)
                    return redirect('homeView')
                else:
                    context = {'error':'Invalid credentials!'}
            
    return render(request,'login.html',context=context)

def registerPage(request):
    
    if request.user.is_authenticated:
        return redirect('homeView')
    
    form = CustomUserCreationForm()

    context: dict = {"form":form}

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)
            return redirect('homeView')
        
        else:
            context.update({'errors':form.error_messages.values()})   


    return render(request,'register.html',context=context)

@login_required(login_url='login')
def logoutPage(request):
    logout(request)

    return redirect('login')