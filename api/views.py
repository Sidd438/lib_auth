from django.shortcuts import render
from .serializers import BookSerializer
from django.http import JsonResponse
from lib_app.models import Book
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import LibrariansOnly

class BookViewSet(viewsets.ModelViewSet):
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes=[LibrariansOnly]



class BookList(APIView):
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