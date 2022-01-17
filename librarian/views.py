from django.shortcuts import render, redirect
from lib_app.models import Issue
from lib_app.forms import UploadFileForm
from django.contrib.auth import authenticate, login, logout
from datetime import datetime, timedelta
from .utils import lib_data, process_renew_request, process_return, send_mail, handle_uploaded_file
from librarian.forms import BookForm
from librarian.models import Libdata
from allauth.socialaccount.models import SocialAccount
from django.contrib import messages


def logoutA(request):
    logout(request)
    return redirect('/librarian')


def logina(request):
    return render(request, 'liblogin.html')


def logging(request):
    user = request.user
    if(request.method == 'POST'):
        form = BookForm(request.POST)
        if(form.is_valid()):
            form.save()
            user.libdata.books_added += 1
            user.libdata.save()
    if(request.POST.get("password")):
        user = authenticate(username=request.POST.get(
            "name"), password=request.POST.get("password"))
        if(user):
            if(user.groups.filter(name="Librarians").exists()):
                login(request,user)
                return libInterface(request)
        return render(request, "error.html")
    elif(request.FILES):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.user,request.FILES['file'])
        else:
            messages.add_message(request, messages.INFO, 'Wrong File Extension')
    elif(request.POST.get('time')):
        time = request.POST.get('time')
        issue_id = request.POST.get('issue_id')
        try:
            record = Issue.objects.filter(id=issue_id).first()
            book = record.book
            dt = datetime.now()
            td = timedelta(days=int(time))
            my_date = dt + td
            record.due_date = my_date
            record.pending = False
            record.issued = True
            record.save()
            book.issues += 1
            book.available = False
            book.save()
            print("lop")
            user.libdata.books_issued += 1
            user.libdata.save()
            msg = "Subject: Book Issued\n\n You have been Issued " + book.name + " for "+time+" day/s"
            email = SocialAccount.objects.filter(user=record.user).first().extra_data['email']
            send_mail(email, msg)
        except:
            pass
    elif(request.POST.get('reason')):
        issue_id = request.POST.get('issue_id')
        record = Issue.objects.get(id=issue_id)
        try:
            book = record.book
            record.pending = False
            record.denied = True
            record.active = False
            record.reason = request.POST.get('reason')
            record.save()
            msg = "Subject: Book Denied\n\n Your request for " + \
                book.name + " has been denied because " + record.reason 
            email = SocialAccount.objects.filter(
                user=record.user).first().extra_data['email']
            send_mail(email,msg)
        except:
            pass
    elif(request.POST.get('merit')):
        try:
            process_return(request.POST.get("issue_id"),request.POST.get("merit"))
        except:
            pass
    elif(request.POST.get('accept')):
        try:    
            print("lok")
            process_renew_request(request.POST.get('timed'), True)
        except:
            pass    
    elif(request.POST.get('decline')):
        try:
            print("kok")
            process_renew_request(request.POST.get('timed'), False)
        except:
            pass    
    return libInterface(request)

def libInterface(request):
    current_user = request.user
    if(current_user.is_anonymous):
        return redirect('/librarian')
    context = lib_data()
    return render(request, "libinterface.html", context)

def profile(request):
    current_user = request.user
    if(current_user.is_anonymous):
        return redirect('/librarian')
    return render(request, 'lib_profile.html',{'user':request.user})