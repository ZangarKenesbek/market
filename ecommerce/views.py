from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from products.forms import CreateUserForm


@login_required
def profile(request):
    return render(request,'profile.html')


def registration(request):
    form = CreateUserForm()
    if request.method == "POST":

        form = CreateUserForm(request.POST)

        if form.is_valid():

            form.save()
            return redirect("profile")
    context = {
        'registrationform': form
    }
    return render(request, 'registration/registration.html', context=context)