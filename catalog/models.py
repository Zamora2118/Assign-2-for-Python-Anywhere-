# catalog/models.py
from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.urls import reverse


class Genre(models.Model):
    """Model representing a book genre (e.g. Science Fiction)."""
    name = models.CharField(max_length=200, help_text="Enter a book genre (e.g. Science Fiction)")

    def __str__(self):
        return self.name


class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)
    author_image = models.ImageField(upload_to='images/authors/', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this author."""
        return reverse('catalog:author_detail', args=[str(self.id)])


class Book(models.Model):
    """Model representing a book (but not a specific copy)."""
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN', max_length=13, unique=True)
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    book_image = models.ImageField(upload_to='images/books/', null=True, blank=True)  # ✅ New field

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this book."""
        return reverse('catalog:book_detail', args=[str(self.id)])


class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e., that can be borrowed)."""
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    @property
    def is_overdue(self):
        return bool(self.due_back and date.today() > self.due_back)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        return f'{self.id} ({self.book.title})'
