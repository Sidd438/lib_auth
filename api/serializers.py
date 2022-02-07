from rest_framework import serializers
from lib_app.models import Book, Issue, Review
from django.contrib.auth.models import User


class RegestrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)

    class Meta:
        model = User
        fields =['username','email','password','password2']
        extra_kwargs = {
            'password': {'write_only':True}
        }

    def save(self, **kwargs):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if(password != password2):
            raise serializers.ValidationError({'error':'password and confirm password are not the same'})
        if(User.objects.filter(username=self.validated_data['username']).exists()):
            raise serializers.ValidationError(
                {'error': 'Username aldready exists'})
        user = User.objects.create(username=self.validated_data['username'], email=self.validated_data['email'])
        user.set_password(password)
        user.save()
        return user

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)


    class Meta:
        model = Book
        fields = '__all__'
    

class IssueSerializer(serializers.ModelSerializer):
    book = serializers.CharField(source='book.name', read_only=True)
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Issue
        fields = '__all__'