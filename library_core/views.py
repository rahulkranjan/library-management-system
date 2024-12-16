from datetime import date
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import permissions
from library_core.models import Author, Book, BorrowRecord
from library_core.serializers import AuthorGetSerializer, AuthorSerializer, BookGetSerializer, BookSerializer, BorrowRecordSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from django.http import FileResponse
import os
from library_core.tasks import generate_report


# Create your views here.
class AuthorsList(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AuthorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']

    search_fields = {
        'name': ['icontains'],
    }

    def get_queryset(self):
        queryset = Author.objects.filter().order_by('-created_at')
        return queryset

    def post(self, request, format=None):
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully.','data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Something went wrong', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AuthorsDetailed(APIView):

    def get_object(self, pk):
        try:
            return Author.objects.get()
        except Author.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        book = self.get_object(pk)
        serializer = AuthorGetSerializer(book)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        val = self.get_object(pk)
        serializer = AuthorSerializer(
            val, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        val = self.get_object(pk)
        val.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class BooksList(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id', 'author']
    search_fields = {
        'title': ['icontains'],
    }

    def get_queryset(self):
        queryset = Book.objects.filter().order_by('-created_at')
        return queryset
    
    def post(self, request, format=None):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Book created successfully.','data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Something went wrong', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

class BooksDetailed(APIView):
    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
        book = self.get_object(pk)
        serializer = BookGetSerializer(book)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        book = self.get_object(pk)
        serializer = BookSerializer(
            book, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        book = self.get_object(pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class BorrowRecordsList(APIView):
    def post(self, request, format=None):
        serializer = BorrowRecordSerializer(data=request.data)
        if serializer.is_valid():
            book_id = request.data.get('book')
            book = Book.objects.get(id=book_id)
            
            if book.available_copies > 0:
                book.available_copies -= 1 
                book.save()
                serializer.save()
                return Response({'message': 'Borrow record created successfully.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'No available copies for this book.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Something went wrong', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ReturnBorrowedBookAPIView(APIView):
    def put(self, request, pk):
        try:
            borrow_record = BorrowRecord.objects.get(id=pk)
        except BorrowRecord.DoesNotExist:
            return Response({"detail": "Borrow record not found."}, status=status.HTTP_404_NOT_FOUND)

        borrow_record.return_date = date.today()
        borrow_record.book.available_copies += 1
        borrow_record.book.save()
        borrow_record.save()
        return Response({'message': 'Book returned successfully!'}, status=status.HTTP_200_OK)
    

class GenerateReportAPIView(APIView):
    def get(self, request, format=None):
        report_dir = 'reports'
        report_files = sorted(os.listdir(report_dir), reverse=True)
        
        if report_files:
            latest_report = os.path.join(report_dir, report_files[0])
            return FileResponse(open(latest_report, 'rb'), as_attachment=True, content_type='application/json')
        return Response({'message': 'No reports found.'}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request, format=None):
        task = generate_report.delay()
        return Response({'message': 'Report generation started.', 'task_id': task.id}, status=status.HTTP_202_ACCEPTED)
    

    