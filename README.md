# **Library Management System**

This project is a **Library Management System** API built using **Django**, **Django REST Framework (DRF)**, and **Celery**. It allows users to manage books and authors, track book borrowing records, and generate periodic reports on library activity.

---

## **Features**

### **API Endpoints**
1. **Authors**
   - `GET /authors/` - List all authors.
   - `POST /authors/` - Create a new author.
   - `GET /authors/<id>/` - Retrieve a specific author.
   - `PUT /authors/<id>/` - Update a specific author.
   - `DELETE /authors/<id>/` - Delete a specific author.

2. **Books**
   - `GET /books/` - List all books.
   - `POST /books/` - Add a new book.
   - `GET /books/<id>/` - Retrieve a specific book.
   - `PUT /books/<id>/` - Update a specific book.
   - `DELETE /books/<id>/` - Delete a specific book.

3. **Borrow Records**
   - `POST /borrow-record/` - Create a borrow record (decreases `available_copies` by 1 if copies are available).
   - `PUT /borrow-record/<id>/return/` - Update a borrow record, e.g., adding a return date.

4. **Reports**
   - `POST /reports/` - Trigger background task to generate a library activity report.
   - `GET /reports/` - Download the latest report.

---

## **Tech Stack**
- **Backend**: Django, Django REST Framework
- **Task Queue**: Celery with Redis
- **Database**: Postgres
- **Containerization**: Docker

---

## **Setup and Installation**

### **Prerequisites**
- Python 3.10 or higher
- Redis (for Celery backend)
- Docker (optional, for containerized deployment)



### **Steps**
1. Clone the repository:
   ```bash
   git clone https://github.com/rahulkranjan/library-management-system.git
   cd library-management

2. Install dependencies:
   ```bash
   pip install -r requirements.txt

3. Start the development server:
   ```bash
    python manage.py runserver

4. Start the Redis server Ensure Redis is running. If not installed, use Docker:
   ```bash
    docker run -d -p 6379:6379 redis

5. Start the Celery worker
    ```bash
    celery -A library_management worker --loglevel=info