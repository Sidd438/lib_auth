from django.shortcuts import render
from lib_app.models import Book, Issue, Issued, Denied
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import logout
from django.shortcuts import redirect
from allauth.account.admin import EmailAddress

def logoutA(request):
    logout(request)
    return redirect('/accounts/login')

def red(request):
    return redirect('/accounts/login')

def home(request):
    name = request.user.username
    current_user = request.user
    try:
        data = SocialAccount.objects.get(user=request.user).extra_data
        email = data.get('email')
        if "@pilani.bits-pilani.ac.in" not in email:
            current_user.delete()
            return render(request,'error.html')
    except:
        pass
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
    if(EmailAddress.objects.filter(user=request.user, verified=True).exists()):
        pass
    else:
        return render(request,'error_reg.html')
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
        if not(Issued.objects.filter(username=name, book_name=book_name).exists() or Issue.objects.filter(username=name, book_name=book_name).exists()):
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
    current_user = request.user
    issue = None
    try:
        issue = Issued.objects.filter(username=current_user.username)
    except:
        pass
    data = SocialAccount.objects.get(user=current_user).extra_data
    data['bits_id'] = current_user.profile.bits_id
    data['hostel'] = current_user.profile.hostel
    data['room_no'] = current_user.profile.room_no
    data['phone_number'] = current_user.profile.phone_number
    data['issueds'] = issue

    return render(request,'profile.html',data)

def editprofile(request):
    user = request.user
    if(request.POST.get('bits_id')):
        user.profile.bits_id = request.POST.get('bits_id')
        user.save()
    if(request.POST.get('hostel')):
        user.profile.hostel = request.POST.get('hostel')
        user.save()
    if(request.POST.get('room_number')):
        user.profile.room_no = request.POST.get('room_number')
        user.save()
    if(request.POST.get('phone_number')):
        user.profile.phone_number = request.POST.get('phone_number')
        user.save()
    return render(request,'editor.html')
