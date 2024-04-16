from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from .forms import SignupForm, LoginForm
from .models import Planet, PlanetBase, FlightSchedule
from django.core.exceptions import ObjectDoesNotExist
import datetime

# Create your views here.
def index(request):
    return render(request, 'index.html')

# signup page
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

# login page
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# logout page
def logout_view(request):
    logout(request)
    return redirect('login')

#booking page

def booking_view(request):
    planets = Planet.objects.all()
    if request.method == 'POST':
        planet_id = request.POST.get('planet_id')
        planet = Planet.objects.get(id=planet_id)
        request.session['planet_id'] = planet.id
        request.session['fare'] = planet.fare
        return redirect('checkout')
    return render(request, 'booking.html', {'planets': planets})

def select_base(request):
    if request.method == 'POST':
        planet_id = request.POST.get('planet_id')
        planet = Planet.objects.get(id=planet_id)
        bases = planet.bases.all()
        if request.POST.get('base_id'):
            base_id = request.POST.get('base_id')
            base = PlanetBase.objects.get(id=base_id)
            request.session['base_id'] = base.id
            request.session['planet_id'] = planet.id
            return redirect('select_date')
        return render(request, 'select_base.html', {'planet': planet, 'bases': bases})
    return render(request, 'booking.html', {'planets': planet})


# def select_date(request):
#     print(request.method)
#     if request.method == 'GET':
#         print("hi1")
#         planet_id = request.session.get('planet_id')
#         planet = Planet.objects.get(id=planet_id)
#         bases = planet.bases.all()
#         source_base_id = 13  # Assuming California Base has ID 13
#         base_id = request.session['base_id']
#         print("base_id", base_id)
#         if request.session['base_id']:
#             print("hi2")
#             #base_id = request.POST.get('base_id')
#             base = PlanetBase.objects.get(id=base_id)
#             request.session['base_id'] = base.id
#             return render(request, 'select_dates.html', {'planet': planet, 'source_base_id': source_base_id})
#         return render(request, 'flight_list.html', {'planet': planet, 'bases': bases})
#     else:  # Handle GET request
#         print("hi3")
#         # Set default source base to California Base
#         source_base_id = 13  # Assuming California Base has ID 13
#         planet_id = request.session.get('planet_id')
#         planet = Planet.objects.get(id=planet_id)
#         return render(request, 'flight_list.html', {'planet': planet, 'source_base_id': source_base_id})

def select_date(request):
    if request.method == 'POST':
        planet_id = request.session.get('planet_id')
        planet = Planet.objects.get(id=planet_id)
        bases = planet.bases.all()
        source_base_id = 13  # Assuming California Base has ID 13
        if 'base_id' in request.session:
            base_id = request.session['base_id']
            base = PlanetBase.objects.get(id=base_id)
            request.session['base_id'] = base.id
        else:
            base = PlanetBase.objects.get(id=source_base_id)
            request.session['base_id'] = base.id
        return render(request, 'select_dates.html', {'planet': planet, 'source_base_id': source_base_id})
    else:
        # Handle POST request
        return redirect('flight_list')
    
# def flight_list(request):
#     print("outside if", )
#     if request.method == 'GET':
#         departure_date_str = request.POST.get('departure_date')
#         arrival_date_str = request.POST.get('arrival_date')
        
#         # Convert date strings to datetime objects
#         departure_date = datetime.strptime(departure_date_str, '%Y-%m-%d')
#         print("dd", departure_date)
#         arrival_date = datetime.strptime(arrival_date_str, '%Y-%m-%d')
#         print("ad", arrival_date)
        
#         # Set default value for arrival_base_id
#         arrival_base_id = 13
        
#         # Get destination_base_id from session
#         destination_base_id = request.session.get('base_id')
        
#         # Query flights based on departure and arrival dates, and destination base
#         flights = FlightSchedule.objects.filter(departure_date=departure_date, 
#                                                  arrival_date=arrival_date, 
#                                                  destination_base_id=destination_base_id, 
#                                                  arrival_base_id=arrival_base_id)
        
#         return render(request, 'flight_list.html', {'flights': flights})
#     else:
#         # Redirect to the page where user selects departure and arrival dates
#         return redirect('select_dates')
    
def flight_list(request):
    planet_id = request.session.get('planet_id')
    planet = Planet.objects.get(id=planet_id)
    source_base_id = 13  # Assuming California Base has ID 13
    if request.method == 'POST':
        departure_date_str = request.POST.get('departure_date')
        arrival_date_str = request.POST.get('arrival_date')
        # Convert date strings to datetime objects
        departure_date = datetime.datetime.strptime(departure_date_str, '%Y-%m-%d')
        arrival_date = datetime.datetime.strptime(arrival_date_str, '%Y-%m-%d')
        # Get destination_base_id from session
        destination_base_id = request.session.get('base_id')
        # Query flights based on departure and arrival dates, and destination base
        flights = FlightSchedule.objects.filter(
            departure_date=departure_date,
            arrival_date=arrival_date,
            destination_base_id=destination_base_id
        )
        return render(request, 'flight_list.html', {'flights': flights})
    else:
        # Redirect to the page where user selects departure and arrival dates
        return render(request, 'select_dates.html', {'planet': planet, 'source_base_id': source_base_id})
    
def payment_page(request):
    return render(request, 'payment_page.html')

def process_payment(request):
    return redirect(request, 'process_payment.html')