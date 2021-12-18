from django.shortcuts import render
from librarian.models import Librarian
from lib_app.models import Issue, Issued, Denied, Book
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
        record = Issue.objects.get(username=username, book_id=book_id)
        record.delete()
        dt = datetime.now()
        td = timedelta(days=int(time))
        my_date = dt + td
        issued = Issued.objects.create(username=username, book_name=book_name, book_id=book_id, time=time, due_date=my_date)
        issued.save()
        book = Book.objects.get(name=book_name)
        print(book)
        book.available = False
        book.save(update_fields=['available'])
        return libInterface(request)
    elif(request.POST.get('reason')):
        username = request.POST.get('username')
        book_name = request.POST.get('book_name')
        book_id = request.POST.get('book_id')
        reason = request.POST.get('reason')
        record = Issue.objects.get(username=username, book_id=book_id)
        record.delete()
        denied = Denied.objects.create(
            username=username, book_name=book_name, book_id=book_id, reason=reason)
        denied.save()
        return libInterface(request)
    elif(request.POST.get('genre')):
        book_name = request.POST.get('book_name')
        image_link = request.POST.get('image_link')
        summary = request.POST.get("summary")
        author = request.POST.get('author')
        isbn = request.POST.get('isbn')
        genre = request.POST.get('genre')
        book = Book.objects.create(image_link=image_link, name=book_name,
                                   summary=summary, author=author, isbn=isbn, genre=genre)
        book.save()
        return libInterface(request)


def libInterface(request):
    IssueA = Issue.objects.all()
    issues = []
    for issue in IssueA:
        issues.append(issue)
    context = {'issues': issues}
    return render(request, "libinterface.html", context)
