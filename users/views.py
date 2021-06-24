from django.shortcuts import render
# from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DetailView, UpdateView, ListView, DeleteView
from django.shortcuts import redirect
from .forms import *
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .filters import *
from .models import *
from django.urls import reverse, reverse_lazy
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
User = get_user_model()
# Create your views here.

def home(request):
    return render(request, 'users/index.html')

def about(request):
    return render(request, 'users/about.html')

@login_required
def dlawyers(request):
    lawyers = User.objects.filter(user_type=2)
    ctx = {
        'lawyers' : lawyers
    }
    return render(request, 'users/dashboard/lawyer.html', context=ctx)

@login_required
def dclients(request):
    clients = User.objects.filter(user_type=3)
    ctx = {
        'clients' : clients
    }
    return render(request, 'users/dashboard/client.html', context=ctx)

@login_required
def dashboard(request):
    lawyers = User.objects.filter(user_type=2)
    clients = User.objects.filter(user_type=3)
    tlawyers = User.objects.filter(user_type=2).count()
    tclients = User.objects.filter(user_type=3).count()
    bookings = Booking.objects.count()
    reviews = Review.objects.count()
    
    ctx = {
        'lawyers' : lawyers,
        'clients' : clients,
        'tlawyers' : tlawyers,
        'tclients' : tclients,
        'bookings' : bookings,
        'reviews' : reviews,
    }
    return render(request, 'users/dashboard/index.html', context=ctx)

class LawyerRegistrationView(CreateView):
    model = User
    form_class = LawyerRegistrationForm
    template_name = 'users/lawyer.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.user_type = 2
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        return super().form_valid(form)

class RegistrationView(LoginRequiredMixin, CreateView):
    model = User
    form_class = AdminRegistrationForm
    template_name = 'users/dashboard/user_reg.html'
    success_url = reverse_lazy('dashboard')


class ClientRegistrationView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'users/client.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.user_type = 3
        return super().form_valid(form)

class UserLoginView(LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        nxt = self.request.GET.get("next", None)
        if nxt:
            return "%s" % (nxt)
        if self.request.user.user_type == 1:
            return reverse_lazy('dashboard')
        return reverse_lazy('home')

class LawyerDetailView(DetailView):
    model = User
    context_object_name = 'lawyer'
    template_name = 'users/lawyer_details.html'

    def get_context_data(self, **kwargs):
        obj = self.get_object()
        kwargs['reviews'] = Review.objects.filter(booking__lawyer=self.kwargs['pk'])
        kwargs['expertareas'] = ExpertArea.objects.filter(user=self.kwargs['pk'])
        bookings = Booking.objects.filter(client=self.request.user)
        for b in bookings:
            if b.lawyer == obj:
                kwargs['booking'] = b
        return super().get_context_data(**kwargs)

class ProfileView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'user'

    def test_func(self):
        obj = self.get_object()
        if self.request.user == obj:
            return True
        return False

    def get_context_data(self, **kwargs):
        if self.request.user.user_type == 3:
            bookings = Booking.objects.filter(client=self.request.user)
        elif self.request.user.user_type == 2:
            bookings = Booking.objects.filter(lawyer=self.request.user)
        kwargs['bookings'] = bookings
        return super().get_context_data(**kwargs)

def search(request):
    lawyers = User.objects.filter(user_type=2)
    lawyerFilter = LawyerFilter(request.GET, queryset=lawyers)
    lawyers = lawyerFilter.qs
    ctx = {
        'lawyers' : lawyers,
        'lawyerFilter': lawyerFilter
    }
    return render(request, 'users/search.html', context=ctx)

class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'users/booking_create.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.lawyer, user = User.objects.get(id=self.kwargs['pk'])
        form.instance.client, client = self.request.user
        date = form.cleaned_data['date']
        amount = form.cleaned_data['amount']
        service = form.cleaned_data['service']
        status = form.cleaned_data['status']
        mail_subject = "New Client Schedule"
        messege = render_to_string('users/email.html', {
            'user' : user,
            'client' : client,
            'date' : date,
            'service' : service,
            'amount' : amount
        })
        to_email = user.email
        email = EmailMessage(mail_subject, messege, to=[to_email])
        email.send()
        return super().form_valid(form)

class AdminBookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = AdminBookingForm
    template_name = 'users/dashboard/booking_create.html'
    success_url = reverse_lazy('dashboard')

class AdminBookingUpdateView(LoginRequiredMixin, UpdateView):
    model = Booking
    form_class = AdminBookingForm
    template_name = 'users/dashboard/booking_update.html'
    success_url = reverse_lazy('dashboard')


class AdminBookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'users/dashboard/booking.html'
    context_object_name = 'bookings'


class BookingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Booking
    form_class = BookingUpdateForm
    template_name = 'users/booking_update.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        
        return super().form_valid(form)

    def test_func(self):
        if self.request.user.user_type == 1:
            return True
        return False

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'users/review.html'

    def form_valid(self, form):
        form.instance.booking = Booking.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('user-profile', kwargs={'pk' : self.request.user.id})

class ExpertAreaCreateView(LoginRequiredMixin, CreateView):
    model = ExpertArea
    form_class = ExpertAreaForm
    template_name = 'users/expert.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('user-profile', kwargs={'pk' : self.request.user.id})


class UserDelete(DeleteView):
    model = User
    success_url = reverse_lazy('dashboard')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class CleintUpdateView(UpdateView):
    model = User
    form_class = UpdateForm
    context_object_name = 'user'
    template_name = 'users/dashboard/client_update.html'
    success_url = reverse_lazy('dashboard')

class LawyerUpdateView(UpdateView):
    model = User
    form_class = LawyerUpdateForm
    context_object_name = 'user'
    template_name = 'users/dashboard/lawyer_update.html'
    success_url = reverse_lazy('dashboard')