from django.shortcuts import render
from lib_app.models import Issue, Book, Renew, Spreadsheet
from lib_app.forms import UploadFileForm
from django.contrib.auth import authenticate
from datetime import datetime, timedelta
from django.contrib.auth import logout
from django.shortcuts import redirect
from allauth.socialaccount.models import SocialAccount
from django.core.mail import send_mail



def logoutA(request):
    logout(request)
    return redirect('/librarian')


def login(request):
    return render(request, 'liblogin.html')


def logging(request):
    user = request.user
    if(user.is_anonymous):
        return redirect('/')
    if(request.POST.get("password")):
        user = authenticate(username=request.POST.get(
            "name"), password=request.POST.get("password"))
        if(user):
            if(user.groups.filter(name="Librarians").exists()):
                return libInterface(request)
        return render(request, "error.html")
    elif(request.FILES):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
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
            '''send_mail("Books Issued", "You have been Issued "+book_name +
                      " for "+time+" day/s", "", [email], fail_silently=False)'''
        except:
            pass
    elif(request.POST.get('reason')):
        issue_id = request.POST.get('issue_id')
        record = Issue.objects.get(id=issue_id)
        try:
            record.pending = False
            record.denied = True
            record.reason = request.POST.get('reason')
            record.save()
        except:
            print('pop')
            pass
    elif(request.POST.get('merit')):
        issue_id = request.POST.get('issue_id')
        merit = request.POST.get('merit')
        try:
            returned = Issue.objects.get(id=issue_id)
            returned.returned = False
            returned.active = False
            returned.save()
            user = returned.user
            user.profile.merit = (user.profile.merit *user.profile.returns+int(merit))/(user.profile.returns+1)
            user.profile.returns += 1
            user.save()
        except:
            pass
    elif(request.POST.get('accept')):
        try:    
            renew = Renew.objects.get(id=request.POST.get('timed'))
            issued = renew.issue
            td = timedelta(days=int(renew.time))
            issued.due_date = issued.due_date + td
            issued.save()
            renew.delete()
        except:
            pass    
    elif(request.POST.get('decline')):
        try:    
            renew = Renew.objects.get(id=request.POST.get('timed'))
            renew.delete()
        except:
            pass    

    return libInterface(request)

def libInterface(request):
    ReturnedsA = Issue.objects.filter(returned=True)
    IssuesA = Issue.objects.filter(pending=True)
    RenewsA = Renew.objects.all()
    form = UploadFileForm()
    context = {'issues': IssuesA, 'returneds':ReturnedsA, 'renews': RenewsA, 'form':form}
    return render(request, "libinterface.html", context)

def handle_uploaded_file(spreadsheet):
    pass