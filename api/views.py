from .serializers import BookSerializer, IssueSerializer, RegestrationSerializer
from lib_app.models import Book, Issue
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework import viewsets
from .permissions import LibrariansOnly
from rest_framework.authtoken.models import Token
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status

class IssueList(ListCreateAPIView):
    serializer_class = IssueSerializer
    permission_classes = [LibrariansOnly]
    queryset = Issue.objects.all()


class IssueDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = IssueSerializer
    permission_classes = [LibrariansOnly]

    def get_object(self):
        issue = Issue.objects.filter(id = self.kwargs['pk']).first()
        return issue


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [LibrariansOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['active', 'pending', 'issued', 'denied', 'returned']



class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes=[LibrariansOnly]



class BookList(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        permission_classes=[LibrariansOnly]
        return Response(serializer.data)
    
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        permission_classes = [LibrariansOnly]
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class BookDetail(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get(self, request, isbn):
        book = Book.objects.get(isbn=isbn)
        serializer = BookSerializer(book, many=False)
        permission_classes = [LibrariansOnly]
        return Response(serializer.data)

    def delete(self, request, isbn):
        book = Book.objects.get(isbn=isbn)
        book.delete()
        permission_classes = [LibrariansOnly]
        return Response("Book Has Been Deleted")
    
    def put(self, request, isbn):
        book = Book.objects.get(isbn=isbn)
        serializer = BookSerializer(book, data=request.data)
        permission_classes = [LibrariansOnly]
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class mixinsList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class =BookSerializer
    permission_classes = [LibrariansOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author', '=available']



    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class MixinDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = BookSerializer
    permission_classes = [LibrariansOnly]


    def get_object(self):
        isbn = int(self.kwargs["pk"])
        book = Book.objects.filter(isbn=isbn).first()
        return book

class RegestrationView(APIView):
    def post(request, data):
        serializer = RegestrationSerializer(data=request.data)
        if serializer.is_valid():
            print("ok")
            user = serializer.save()
            return Response(serializer.data)

@api_view(['POST'])
def regestration_func(request):
    serializer = RegestrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        data = serializer.data
        token = Token.objects.get_or_create(user=user).key
        return Response(data)

@api_view(['POST'])
def logoutapi(request):
    if request.method == "POST":
        request.user.auth_token.delete()
        return Response(status = status.HTTP_200_OK)

""" @api_view(['GET'])
def book_api(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def book_detail(request, isbn):
    book = Book.objects.get(isbn=isbn)
    serializer = BookSerializer(book, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def book_create(request):
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST','DELETE'])
def book_update(request, isbn):
    book = Book.objects.get(isbn=isbn)
    if(request.method == 'DELETE'):
        book.delete()
        return Response("Book Deleted")
    serializer = BookSerializer(instance=book, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
 """