from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
    path('lawyer/<int:pk>/', LawyerDetailView.as_view(), name='lawyer-profile'),
    path('lawyer/<int:pk>/book/', BookingCreateView.as_view(), name='lawyer-booking'),
    path('lawyer/book/<int:pk>/update/', BookingUpdateView.as_view(), name='booking-update'),
    path('book/<int:pk>/review/', ReviewCreateView.as_view(), name='review-create'),
    path('expert-area/create/', ExpertAreaCreateView.as_view(), name='expert-area-create'),
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('admin/', dashboard, name='dashboard'),
    path('dashboard/lawyer/', dlawyers, name='d-lawyer'),
    path('dashboard/client/', dclients, name='d-client'),
    path('dashboard/client/<int:pk>/update/', CleintUpdateView.as_view(), name='dclient-update'),
    path('dashboard/lawyer/<int:pk>/update/', LawyerUpdateView.as_view(), name='dlawyer-update'),
    path('dashboard/user-reg/', RegistrationView.as_view(), name='user-reg'),
    path('dashboard/booking/all/', AdminBookingListView.as_view(), name='all-bookings'),
    path('dashboard/booking/create/', AdminBookingCreateView.as_view(), name='abooking-create'),
    path('dashboard/booking/update/<int:pk>', AdminBookingUpdateView.as_view(), name='abooking-update'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('lawyer/', LawyerRegistrationView.as_view(), name='lawyer-reg'),
    path('client/', ClientRegistrationView.as_view(), name='client-reg'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='user-profile'),
    path('profile/<int:pk>/delete/', UserDelete.as_view(), name='user-delete'),
    path('search/', search, name='search'),
]