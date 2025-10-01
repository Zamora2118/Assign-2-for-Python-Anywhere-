from django.urls import path
from . import views  # ✅ CORRECT: Imports views.py from the current directory (the 'register' app)

urlpatterns = [
    # ... your path definitions ...
    path('register/', views.register, name='register'),
]