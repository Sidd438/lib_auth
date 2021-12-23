from django.shortcuts import render
from lib_app.models import Book, Issue, Rating, Renew, Review
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import logout
from django.shortcuts import redirect
from allauth.account.admin import EmailAddress
from .forms import RatingForm

def logoutA(request):
    logout(request)
    return redirect('/accounts/login')


def red(request):
    return render(request,'main.html')


def home(request):
    current_user = request.user
    if(current_user.is_anonymous):
        return redirect('/')
    booksA = Book.objects.all()
    books = []
    books2 = []
    for book in booksA:
        books.append(book)
    if(request.POST.get("search")):
        search_query = request.POST.get("search")
        search_query = search_query.lower()
        for book in books:
            if(search_query in book.name.lower() or search_query in book.author.lower()):
                books2.append(book)
        context = {'books': books2}
        return render(request, 'search.html', context)
    try:
        issuedsA = Issue.objects.filter(user=current_user, issued=True)
    except:
        issuedsA = []
    try:
        deniedsA = Issue.objects.filter(user=current_user, denied=True)
        if(len(deniedsA) > 4):
            deniedsA = deniedsA[0:4]
    except:
        deniedsA = []
    if(len(books) > 3):
        new_books = books[-3:]
    else:
        new_books = books
    trending = books
    trending.sort(key=lambda x: x.issues, reverse=True)
    trending = trending[0:3]
    context = {'books': booksA, 'issueds': issuedsA,
               'd': deniedsA, 'new': new_books, 'trending':trending}
    return render(request, 'home.html', context)


def book_profile(request):
    current_user = request.user
    if(current_user.is_anonymous):
        return redirect('/')
    if(EmailAddress.objects.filter(user=request.user, verified=True).exists()):
        pass
    else:
        return render(request, 'error_reg.html')
    if(request.POST.get('ratingd')):
        book = Book.objects.get(id=request.POST.get("ratingd"))
        ratingform = RatingForm(request.POST)
        if ratingform.is_valid:
            ratingform.save()
            rating = Rating.objects.latest('id')
            rate = rating.rating
            rating.user = current_user
            rating.book = book
            rating.save()
            book.brating = (book.brating*book.bratings + rate)/(book.bratings+1)
            book.bratings += 1
            book.save()
    elif(request.POST.get('return')):
        book = Book.objects.get(id=request.POST.get('id'))
        print(book)
        issue = Issue.objects.get(
            user=current_user, book=book, issued=True)
        issue.issued = False
        issue.returned = True
        issue.save()
        book.available = True
        book.save()
    elif(request.POST.get('time')):
        book_id = request.POST.get('id')
        time = request.POST.get('time')
        book = Book.objects.get(id=book_id)
        if not(Issue.objects.filter(user=current_user, book=book, active=True).exists()):
            issue = Issue.objects.create(
                time=time, user=current_user, book=book)
            issue.save()
    elif(request.POST.get('review')):
        book_id = request.POST.get('book_id')
        book = Book.objects.get(id=book_id)
        review = request.POST.get('review')
        rev = Review.objects.create(book=book, user=current_user, review=review)
        rev.save()
    elif(request.POST.get('renew')):
        book =Book.objects.get(id=request.POST.get('book_id'))
        issue = Issue.objects.get(book=book, user=current_user, issued=True)
        time = int(request.POST.get('renew'))
        ren = Renew.objects.create(issue=issue, time=time)
        ren.save()
    return book_data(request)


def book_data(request):
    id2 = request.GET['id']
    book = Book.objects.get(id=id2)
    issue = None
    ratingform = RatingForm()
    try:
        issue = Issue.objects.get(user=request.user, book=book, issued=True)
    except:
        print('no')
        pass
    reviews = reversed(book.review_set.all())
    context = {'book': book, 'issue': issue, 'reviews':reviews, 'rating_form':ratingform}
    return render(request, 'book.html', context)


def profile(request):
    current_user = request.user
    if(current_user.is_anonymous):
        return redirect('/')
    if(request.POST.get('bits_id') or request.POST.get('hostel') or request.POST.get('room_number') or request.POST.get('phone_number')):
        user = request.user
        if(user.is_anonymous):
            return redirect('/')
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
    issue = Issue.objects.filter(user=current_user, issued=True)
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
    if(user.is_anonymous):
        return redirect('/')
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

def similar(request):
    book_name = request.POST.get('book_name')
    id = request.POST.get('id')
    books = Book.objects.all()
    print(book_name)
    bookM = Book.objects.get(id=id)
    similar_books = []
    for book in books:
        if(bookM.genre.lower() == book.genre.lower()):
            similar_books.append(book)
    context = {'books':similar_books}
    return render(request, 'similar.html', context)         
    