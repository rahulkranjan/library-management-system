from django.urls import path
from .views import *


urlpatterns = [

    path('author/', AuthorsList.as_view()),
    path('author/<pk>/', AuthorsDetailed.as_view()),

    path('book/', BooksList.as_view()),
    path('book/<pk>/', BooksDetailed.as_view()),

    path('borrow-record/', BorrowRecordsList.as_view()),
    path('borrow-record/<pk>/return/', ReturnBorrowedBookAPIView.as_view()),

    path('reports/', GenerateReportAPIView.as_view()),

]
