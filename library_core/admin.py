from django.contrib import admin
from library_core.models import *
# Register your models here.

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(BorrowRecord)