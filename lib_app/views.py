from django.shortcuts import render
from lib_app.models import Book, Issue, Issued, Denied, Renew, Returned, Review
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
        data = SocialAccount.objects.get(user=current_user).extra_data
        email = data.get('email')
        if "@pilani.bits-pilani.ac.in" not in email:
            current_user.delete()
            return render(request, 'error.html')
    except:
        pass

    booksA = Book.objects.all()
    books = []
    books2 = []
    for book in booksA:
        books.append(book)
    if(request.POST.get("search")):
        search_query = request.POST.get("search")
        search_query = search_query.lower()
        for book in books:
            if(search_query in book.name.lower()):
                books2.append(book)
        context = {'books': books2}
        print(books2)
        return render(request, 'search.html', context)
    uid = SocialAccount.objects.get(user=current_user).uid
    try:
        issuedsA = Issued.objects.filter(uid=uid)
    except:
        issuedsA = []
    try:
        deniedsA = Denied.objects.filter(uid=uid)
        if(len(deniedsA) > 4):
            deniedsA = deniedsA[0:4]
    except:
        deniedsA = []
    if(len(books) > 3):
        new_books = books[-3:]
    else:
        new_books = books
    context = {'books': booksA, 'issueds': issuedsA,
               'd': deniedsA, 'new': new_books}
    return render(request, 'home.html', context)


def book_profile(request):
    name = request.user.username
    current_user = request.user
    uid = SocialAccount.objects.get(user=current_user).uid
    if(EmailAddress.objects.filter(user=request.user, verified=True).exists()):
        pass
    else:
        return render(request, 'error_reg.html')
    if(request.POST.get('rating')):
        book = Book.objects.get(id=request.POST.get("id"))
        rating = request.POST.get('rating')
        try:
            rating = float(rating)
            if(rating <= 5 and rating >= 0):
                print((book.rating*book.reviews+rating)/(book.reviews+1))
                book.rating = (book.rating*book.reviews +
                               rating)/(book.reviews+1)
                book.save()
                buffer = str(book.rating)[0:3]
                print(buffer)
                book.rating = float(buffer)
                book.reviews = 1 + book.reviews
                book.save()
        except:
            pass
    elif(request.POST.get('return')):
        issued = Issued.objects.get(
            uid=uid, book_name=request.POST.get('return'))
        issued.delete()
        book = Book.objects.get(name=request.POST.get('return'))
        returned = Returned.objects.create(
            uid=uid, book_name=book.name, username=name)
        returned.save()
        book.available = True
        book.save(update_fields=['available'])
    elif(request.POST.get('time')):
        book_id = request.POST.get('id')
        uid = SocialAccount.objects.get(user=current_user).uid
        time = request.POST.get('time')
        book_name = Book.objects.get(name=request.POST.get('name')).name
        if not(Issued.objects.filter(username=name, book_name=book_name).exists() or Issue.objects.filter(username=name, book_name=book_name).exists()):
            issue = Issue.objects.create(
                time=time, username=name, book_id=book_id, book_name=book_name, uid=uid)
            issue.save()
    elif(request.POST.get('review')):
        book_name = request.POST.get('book_name')
        review = request.POST.get('review')
        rev = Review.objects.create(book_name=book_name, review=review)
        rev.save()
    elif(request.POST.get('renew')):
        book_name = request.POST.get("bookname")
        print(book_name)
        time = int(request.POST.get('renew'))
        ren = Renew.objects.create(book_name=book_name, time=time)
        ren.save()
    return book_data(request)


def book_data(request):

    id2 = request.GET['id']
    uid = SocialAccount.objects.get(user=request.user).uid
    book = Book.objects.get(id=id2)
    issue = None
    try:
        issue = Issued.objects.get(uid=uid, book_name=book.name)
    except:
        pass
    print(issue)
    context = {'book': book, 'issue': issue}
    return render(request, 'book.html', context)


def profile(request):
    current_user = request.user
    issue = None
    uid = SocialAccount.objects.get(user=current_user).uid
    issue = Issued.objects.filter(uid=uid)
    data = SocialAccount.objects.get(user=current_user).extra_data
    data['bits_id'] = current_user.profile.bits_id
    data['hostel'] = current_user.profile.hostel
    data['room_no'] = current_user.profile.room_no
    data['phone_number'] = current_user.profile.phone_number
    data['merit'] = current_user.profile.merit
    data['issueds'] = issue

    return render(request, 'profile.html', data)


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
    return render(request, 'editor.html')
