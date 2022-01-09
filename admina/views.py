from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User


def logoutA(request):
    logout(request)
    return redirect('/admin')


def logina(request):
    return render(request, 'adminlog.html')


def logging(request):
    current_user = request.user
    form = UserCreationForm()
    if(request.POST.get("password")):
        current_user = authenticate(username=request.POST.get("name"), password=request.POST.get("password"))
        if(current_user):
            if(current_user.groups.filter(name="Admins").exists()):
                login(request, current_user)
            else:
                return render(request, "error.html")
    elif(request.POST.get('librarian')):
        user = User.objects.filter(id=request.POST.get('librarian')).first()
        group = Group.objects.get(name='Librarians')
        group.user_set.add(user)
        user.save()
    elif(request.POST.get('delete')):
        user = User.objects.filter(id=request.POST.get('delete')).first()
        group = Group.objects.get(name='Librarians')
        group.user_set.remove(user)
    elif(request.GET):
        form = UserCreationForm(request.GET)
        if form.is_valid():
            form.save()
    return adminInterface(request, form)


def adminInterface(request, form):
    User = get_user_model()
    users_all = User.objects.exclude(groups__name="Admins")
    librarians = users_all.filter(groups__name="Librarians")
    users = users_all.exclude(groups__name="Librarians")
    context = {'librarians':librarians,'users':users, 'form':form}
    if(request.user.is_anonymous):
        return redirect('/admin')
    return render(request,'adminhome.html',context)