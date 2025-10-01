# catalog/urls.py
from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    # Index/Home Page
    path('', views.index, name='index'),

    # List Views
    path('books/', views.BookListView.as_view(), name='books'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),

    # Detail Views
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author_detail'),

    # User Borrowed Books
    path('my_books/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),

    # Author CRUD
    path('author/create/', views.AuthorCreate.as_view(), name='author_create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author_update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'),

    # Book CRUD
    path('book/create/', views.BookCreate.as_view(), name='book_create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book_update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book_delete'),

    # Loan Book
    path('book/<int:pk>/loan/', views.loan_book_librarian, name='loan_book_librarian'),

    # Available Books
    path('books/available/', views.AvailBooksListView.as_view(), name='all_available'),
]
