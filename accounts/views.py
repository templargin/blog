from django.contrib.auth import login
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import SignUpForm


# Create your views here.


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse('myblog:home'))
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})
