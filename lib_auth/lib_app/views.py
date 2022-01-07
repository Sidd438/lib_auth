from django.contrib import messages
from django.shortcuts import render
from lib_app.models import Book, Issue, Renew, Review
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import logout
from django.shortcuts import redirect
from allauth.account.admin import EmailAddress

from lib_app.utils import process_ratings
from .forms import RatingForm, ProfileForm


def logoutA(request):
    logout(request)
    return redirect('/accounts/login')


def red(request):
    return render(request,'main.html')


def home(request):
    current_user = request.user
    if(current_user.is_anonymous):
        return redirect('/')
    email = SocialAccount.objects.get(user=request.user).extra_data['email']
    if "@pilani.bits-pilani.ac.in" not in email:
        current_user.delete()
        return render(request, 'error.html')
    booksA = Book.objects.filter()
    books2 = []
    if(request.POST.get("search")):
        search_query = request.POST.get("search")
        search_query = search_query.lower()
        for book in booksA:
            if(search_query in book.name.lower() or search_query in book.author.lower()):
                books2.append(book)
        context = {'books': books2}
        return render(request, 'search.html', context)
    issuedsA = Issue.objects.filter(user=current_user, issued=True)
    deniedsA = Issue.objects.filter(user=current_user, denied=True)
    if(len(deniedsA) > 4):
        deniedsA = deniedsA[0:4]
    if(len(booksA) > 3):
        new_books = booksA.order_by('-id')[:3]
    else:
        new_books = booksA
    trending = Book.objects.all().order_by('-issues')
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
            process_ratings(ratingform, book, current_user)
    elif(request.POST.get('return')):
        book = Book.objects.get(id=request.POST.get('id'))
        print(book)
        issue = Issue.objects.get(user=current_user, book=book, issued=True)
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
            issue = Issue.objects.create(time=time, user=current_user, book=book)
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
    else:
        messages.add_message(request, messages.INFO, 'Welcome')
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
    profileform = ProfileForm(initial={'bits_id':user.profile.bits_id, 'hostel':user.profile.hostel, 'room':user.profile.room_no, 'phone_number':user.profile.phone_number})
    if(user.is_anonymous):
        return redirect('/')
    if(request.POST.get('edita_profile')):
        profileform = ProfileForm(request.POST)
        if(profileform.is_valid()):
            if(profileform.cleaned_data.get("bits_id")):
                user.profile.bits_id = profileform.cleaned_data.get("bits_id")
                user.save()
            if(profileform.cleaned_data.get("hostel")):
                user.profile.hostel = profileform.cleaned_data.get("hostel")
                user.save()
            if(profileform.cleaned_data.get("room")):
                user.profile.room_no = profileform.cleaned_data.get("room")
                user.save()            
            if(profileform.cleaned_data.get("phone_number")):
                user.profile.phone_number = profileform.cleaned_data.get("phone_number")
                user.save()
        else:
            for x in profileform.errors:
                if("bits_id" in x):
                    messages.add_message(request, messages.INFO, "Invalid BITS ID")
                if("hostel" in x):
                    messages.add_message(request, messages.INFO, "Invalid Hostel Name")

    context = {'profile_form': profileform, 'user':user}
    return render(request, 'editor.html',context)

def similar(request):
    id = request.POST.get('id')
    books = Book.objects.all()
    bookM = Book.objects.get(id=id)
    similar_books = []
    for book in books:
        if(bookM.genre.lower() == book.genre.lower()):
            similar_books.append(book)
    context = {'books':similar_books}
    return render(request, 'similar.html', context)         
    