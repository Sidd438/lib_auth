from rest_framework import serializers
from lib_app.models import Book, Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)


    class Meta:
        model = Book
        fields = '__all__'
    