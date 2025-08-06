from django.urls import path
from .views import FitnessClassListView, BookingCreateView, client_bookings

urlpatterns = [
    path('classes/', FitnessClassListView.as_view()),
    path('book/', BookingCreateView.as_view()),
    path('bookings/', client_bookings),
]
