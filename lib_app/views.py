from django.shortcuts import render
from lib_app.models import Book, Issue, Issued, Denied
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import logout
from django.shortcuts import redirect
# Create your views here.

def logoutA(request):
    logout(request)
    return redirect('/accounts/login')


def home(request):
    name = request.user.username
    current_user = request.user
    try:
        data = SocialAccount.objects.get(user=request.user).extra_data
        email = data.get('email')
        if "@pilani.bits-pilani.ac.in" not in email:
            return render(request,'error.html')
    except:
        print(SocialAccount.objects.get(user=request.user).extra_data)
    email = current_user.email
    booksA = Book.objects.all()
    books = []
    for book in booksA:
        books.append(book)
    try:
        issuedsA = Issued.objects.filter(username=name)
    except:
        issuedsA = []
    try:
        deniedsA = Denied.objects.filter(username=name)
    except:
        deniedsA = []
    print(deniedsA)
    context = {'books':books, 'issueds':issuedsA, 'd':deniedsA,}    
    return render(request,'home.html', context)

def book_profile(request):
    name = request.user.username
    if(request.POST.get('return')):
        issued = Issued.objects.get(username=name, book_name=request.POST.get('return'))
        issued.delete()
        book = Book.objects.get(name=request.POST.get('return'))
        book.available=True
        book.save(update_fields=['available'])
    if(request.POST.get('time')):
        book_id = request.POST.get('id')
        time = request.POST.get('time')
        book_name = Book.objects.get(name=request.POST.get('name')).name
        try:
            Issue.objects.get(username=name, book_name=book_name)
        except:
            issue = Issue.objects.create(time=time, username=name, book_id=book_id, book_name=book_name)
            issue.save()
    return book_data(request)

def book_data(request):
    id2 = request.GET['id']
    name = request.user.username
    book = Book.objects.get(id=id2)
    issue = None
    try:
        issue = Issued.objects.get(username=name, book_name=book.name)
    except:
        pass
    context = {'book': book, 'issue': issue}
    return render(request, 'book.html', context)

def issue(request):
    book_id = request.POST.get('id')
    time = request.POST.get('time')
    name = request.user.username
    book_name = Book.objects.get(name=request.POST.get('name')).name
    try:
        Issue.objects.get(username=name, book_name=book_name)
    except:    
        issue = Issue.objects.create(time=time,username=name, book_id=book_id, book_name=book_name)
        issue.save()
    book = Book.objects.get(id=book_id)
    issue = None
    try:
        issue = Issued.objects.get(username=name,book_name=book_name)
    except:
        pass    
    context = {'book': book, 'issue':issue}
    return render(request,'book.html',context)

def interface(request):
    name = request.user.username
    book_id = request.POST.get('id')
    book = Book.objects.get(id=book_id)
    issue = None
    try:
        issue = Issued.objects.get(username=name,book_name=book.name)
    except:
        pass    
    context = {'book': book, 'issue':issue}
    return render(request,'book.html',context)

def profile(request):
    data = SocialAccount.objects.get(user=request.user).extra_data
    context = {'data':data}
    return render(request,'profile.html',data)