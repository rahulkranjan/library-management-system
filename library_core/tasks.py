import os
import json
from celery import shared_task
from datetime import datetime
from .models import Author, Book, BorrowRecord

@shared_task
def generate_report():
    report_dir = "reports"
    
    os.makedirs(report_dir, exist_ok=True)

    total_authors = Author.objects.count()
    total_books = Book.objects.count()
    total_borrowed = BorrowRecord.objects.filter(return_date__isnull=True).count()

    report_data = {
        'total_authors': total_authors,
        'total_books': total_books,
        'total_borrowed': total_borrowed,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    report_filename = f"report_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
    report_path = os.path.join(report_dir, report_filename)
    with open(report_path, 'w') as report_file:
        json.dump(report_data, report_file, indent=4)

    return report_filename
