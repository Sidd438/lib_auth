from django.shortcuts import render
from librarian.models import Librarian
from lib_app.models import Issue, Issued, Denied, Book, Returned
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from datetime import datetime, timedelta
from django.contrib.auth import logout
from django.shortcuts import redirect


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
        return libInterface(request)
    elif(request.POST.get('reason')):
        uid = request.POST.get('uid')
        username = request.POST.get('username')
        book_name = request.POST.get('book_name')
        book_id = request.POST.get('book_id')
        reason = request.POST.get('reason')
        record = Issue.objects.get(username=username, book_id=book_id)
        record.delete()
        denied = Denied.objects.create(
            uid=uid, username=username, book_name=book_name, book_id=book_id, reason=reason)
        denied.save()
        return libInterface(request)
    elif(request.POST.get('merit')):
        uid = request.POST.get('uid')
        book_name = request.POST.get('book_name')
        merit = request.POST.get('merit')
        returned = Returned.objects.get(uid=uid,book_name=book_name)
        returned.delete()
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
    context = {'issues': issues, 'returneds':returneds}
    return render(request, "libinterface.html", context)
