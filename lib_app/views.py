from django.shortcuts import render
from lib_app.models import Book, Issue
# Create your views here.
def home(request):
    current_user = request.user
    email = current_user.email
    booksA = Book.objects.all()
    books = []
    for book in booksA:
        books.append(book)
    context = {'books':books}    
    return render(request,'home.html', context)

def book_data(request):
    id2 = request.GET['id']
    book = Book.objects.get(id=id2)
    context = {'book':book}
    return render(request,'book.html',context)

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
    context = {'book': book}
    return render(request,'book.html',context)