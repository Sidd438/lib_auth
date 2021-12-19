from django.shortcuts import render
from librarian.models import Librarian
from lib_app.models import Issue, Issued, Denied, Book, Renew, Returned
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from datetime import datetime, timedelta
from django.contrib.auth import logout
from django.shortcuts import redirect
from allauth.socialaccount.models import SocialAccount



def logoutA(request):
    logout(request)
    return redirect('/librarian')


def login(request):
    return render(request, 'liblogin.html')


def logging(request):
    if(request.POST.get("password")):
        user = authenticate(username=request.POST.get(
            "name"), password=request.POST.get("password"))
        if(user):
            if(user.groups.filter(name="Librarians").exists()):
                return libInterface(request)
        return render(request, "login.html")
    elif(request.POST.get('time')):
        username = request.POST.get('username')
        book_name = request.POST.get('book_name')
        book_id = request.POST.get('book_id')
        time = request.POST.get('time')
        uid = request.POST.get('uid')
        try:
            record = Issue.objects.get(username=username, book_id=book_id)
            record.delete()
            dt = datetime.now()
            td = timedelta(days=int(time))
            my_date = dt + td
            issued = Issued.objects.create(
            uid=uid, username=username, book_name=book_name, book_id=book_id, time=time, due_date=my_date)
            issued.save()
            book = Book.objects.get(name=book_name)
            print(book)
            book.available = False
            book.save(update_fields=['available'])
        except:
            pass
        return libInterface(request)
    elif(request.POST.get('reason')):
        uid = request.POST.get('uid')
        username = request.POST.get('username')
        book_name = request.POST.get('book_name')
        book_id = request.POST.get('book_id')
        reason = request.POST.get('reason')
        try:
            record = Issue.objects.get(username=username, book_id=book_id)
            record.delete()
            denied = Denied.objects.create(
            uid=uid, username=username, book_name=book_name, book_id=book_id, reason=reason)
            denied.save()
        except:
            pass
        return libInterface(request)
    elif(request.POST.get('merit')):
        uid = request.POST.get('uid')
        book_name = request.POST.get('book_name')
        merit = request.POST.get('merit')
        try:
            returned = Returned.objects.get(uid=uid,book_name=book_name)
            returned.delete()
            usersa = SocialAccount.objects.filter(uid=uid)
            usersa = usersa[0]
            user = usersa.user
            user.profile.merit = (user.profile.merit *user.profile.returns+int(merit))/(user.profile.returns+1)
            user.profile.returns += 1
            user.save()
        except:
            pass
        return libInterface(request)
    elif(request.POST.get('accept')):
        book_name = request.POST.get('book_name')
        try:    
            renew = Renew.objects.get(book_name=book_name)
            issued = Issued.objects.get(book_name=book_name)
            td = timedelta(days=int(renew.time))
            issued.due_date = issued.due_date + td
            issued.save()
            renew.delete()
        except:
            pass    
        return libInterface(request)
    elif(request.POST.get('decline')):
        book_name = request.POST.get('book_name')
        try:    
            renew = Renew.objects.get(book_name=book_name)
            renew.delete()
        except:
            pass    
        return libInterface(request)

def libInterface(request):
    ReturnedA = Returned.objects.all()
    returneds = []
    for returned in ReturnedA:
        returneds.append(returned)
    IssueA = Issue.objects.all()
    issues = []
    for issue in IssueA:
        issues.append(issue)
    RenewA = Renew.objects.all()
    renews = []
    for renew in RenewA:
        book_name = renew.book_name
        issued = Issued.objects.get(book_name = book_name)
        renew.username = issued.username
        renew.save()
        renews.append(renew)
    context = {'issues': issues, 'returneds':returneds, 'renews': renews}
    return render(request, "libinterface.html", context)
