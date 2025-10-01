from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
import datetime

from .models import Book, Author, BookInstance, Genre
from .forms import LoanBookForm


# --- Book CRUD ---
class BookCreate(CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'book_image']
    template_name = 'catalog/book_form.html'
    success_url = reverse_lazy('catalog:books')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.save()
        # ✅ handle many-to-many field manually
        for genre in form.cleaned_data['genre']:
            theGenre = get_object_or_404(Genre, name=genre)
            post.genre.add(theGenre)
        post.save()
        return HttpResponseRedirect(self.success_url)


class BookUpdate(UpdateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'book_image']
    template_name = 'catalog/book_form.html'
    success_url = reverse_lazy('catalog:books')

    def form_valid(self, form):
        post = form.save(commit=False)
        # ✅ remove old genres
        for genre in post.genre.all():
            post.genre.remove(genre)
        # ✅ add new genres
        for genre in form.cleaned_data['genre']:
            theGenre = get_object_or_404(Genre, name=genre)
            post.genre.add(theGenre)
        post.save()
        return HttpResponseRedirect(self.success_url)


class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('catalog:books')


# --- Index/Home Page ---
def index(request):
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    return render(request, 'catalog/index.html', {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    })


# --- Book Views ---
class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
    template_name = "catalog/book_list.html"


class BookDetailView(generic.DetailView):
    model = Book
    template_name = "catalog/book_detail.html"


# --- Author Views ---
class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10
    template_name = "catalog/author_list.html"


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = "catalog/author_detail.html"


# --- Loaned Books by User ---
class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(
            borrower=self.request.user,
            status__exact='o'
        ).order_by('due_back')


# --- Author CRUD ---
class AuthorCreate(CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death', 'author_image']
    template_name = 'catalog/author_form.html'
    success_url = reverse_lazy('catalog:authors')


class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death', 'author_image']
    template_name = 'catalog/author_form.html'
    success_url = reverse_lazy('catalog:authors')


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('catalog:authors')


def author_delete(request, pk):
    """Function-based delete with messages."""
    author = get_object_or_404(Author, pk=pk)
    try:
        author.delete()
        messages.success(request, f"{author.first_name} {author.last_name} has been deleted")
    except Exception:
        messages.error(
            request,
            f"{author.first_name} {author.last_name} cannot be deleted. Books exist for this author."
        )
    return redirect('catalog:authors')


# --- Available Books ---
class AvailBooksListView(generic.ListView):
    """Generic class-based view listing all available books."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_available.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status='a').order_by('book__title')


# --- Loan Book Librarian ---
def loan_book_librarian(request, pk):
    """View function for loaning a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = LoanBookForm(request.POST, instance=book_instance)

        if form.is_valid():
            book_instance = form.save(commit=False)
            # ✅ Save borrower from form
            book_instance.borrower = form.cleaned_data['borrower']
            # ✅ Assign due date (4 weeks from today)
            book_instance.due_back = datetime.date.today() + datetime.timedelta(weeks=4)
            # ✅ Mark as On Loan
            book_instance.status = 'o'
            book_instance.save()
            return HttpResponseRedirect(reverse('catalog:all_available'))
    else:
        form = LoanBookForm(instance=book_instance)

    return render(request, 'catalog/loan_book_librarian.html', {'form': form})
