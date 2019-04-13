from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm, LogInForm, UserForm
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect

def register(request):

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = RegistrationForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user_form.cleaned_data['password1'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.accountType=request.POST['accountType']
            #user.accountType=request.POST['accountType']
            #print("Hey",user.accountType)
            print(profile.user)
            '''if 'accountType' in request.POST:
                print('HelloSandip')
                profile.accountType=request.POST['accountType']'''
            profile.save()
            print("Success")
            #registered=True
            messages.success(request, f' Account created for!')

            """if accountType=='Customer':
                return redirect('customer:home')
            if accountType == 'Publisher':
                return redirect('publisher:home')"""
    else:
        user_form = UserForm()
        profile_form = RegistrationForm()
    return render(request, 'website/register.html', {'user_form':user_form,'profile_form':profile_form})



def user_login(request):

    if request.method == "POST":
        login_form = LogInForm(data=request.POST)
        profile_form = RegistrationForm(data=request.POST)
        if login_form.is_valid and profile_form.is_valid:
            username = request.POST.get('username')
            password = request.POST.get('password')
            accountType = request.POST.get('accountType')
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    if(UserProfile.objects.get(user_id=user.id).accountType==accountType):
                        login(request, user)
                        if(accountType=='Publisher'):
                            return redirect('publisher:home')
                        if(accountType=='Customer'):
                            return redirect('customer:home')
                    else:
                        messages.error(request, "Provide valid credentials !!")
            else:
                 messages.error(request, "Provide valid credentials !!")
        else:
            messages.error(request,"Provide valid credentials !!")
            return render(request, "website/login.html", {'login_form' : login_form, 'profile_form' : profile_form})
    else:
        login_form = LogInForm()
        profile_form = RegistrationForm()
    return render(request, "website/login.html",{'login_form':login_form, 'profile_form':profile_form})


@login_required
def user_logout(request):
    logout(request)
    messages.info(request,"Logged  Out Successfully.!!")
    return HttpResponseRedirect(reverse('website:login'))