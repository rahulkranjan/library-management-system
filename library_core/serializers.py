from rest_framework import serializers
from library_core.models import Author, Book, BorrowRecord


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class AuthorGetSerializer(serializers.ModelSerializer):
    books = serializers.SerializerMethodField()
    class Meta:
        model = Author
        fields = '__all__'

    def get_books(self, obj):
        if Book.objects.filter(author=obj.id).exists():
            return Book.objects.filter(author=obj.id).values()
        return []



class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class BookGetSerializer(serializers.ModelSerializer):
    borrower_history = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = '__all__'
        depth = 1

    def get_borrower_history(self, obj):
        if BorrowRecord.objects.filter(book=obj.id).exists():
            return BorrowRecord.objects.filter(book=obj.id).values()
        return []


class BorrowRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRecord
        fields = '__all__'
