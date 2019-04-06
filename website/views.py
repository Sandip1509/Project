from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            accountType = form.cleaned_data.get('accountType')
            messages.success(request, f'Account created for {username}!')
            if accountType=='Customer':
                return redirect('customer:home')
            if accountType == 'Publisher':
                return redirect('publisher:home')
    else:
        form = RegistrationForm()
    return render(request, 'website/register.html', {'form':form})
