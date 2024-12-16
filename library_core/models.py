from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=225)
    bio = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)
    
    class Meta:
        db_table = 'author'


class Book(models.Model):
    title = models.CharField(max_length=225)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='book_author')
    isbn = models.CharField(max_length=13, unique=True)
    available_copies = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)
    
    class Meta:
        db_table = 'book'


class BorrowRecord(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_by = models.CharField(max_length=225)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True)

    def __str__(self):
        return f'{self.book} - {self.borrowed_by}'
    
    class Meta:
        db_table = 'borrow_record'
