from django.shortcuts import render
from .models import Service, Employee, Booking, Customer
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Profile

@login_required
def dashboard_redirect(request):
    user = request.user
    
    if not hasattr(user, 'profile'):
        Profile.objects.create(user=user)
    
    profile = user.profile

    if profile.user_type == 'worker':
        return render(request, 'worker_dashboard.html', {'profile': profile})
    elif profile.user_type == 'customer':
        return render(request, 'dashboard.html', {'profile': profile})
    else:
        return render(request, 'dashboard.html', {'profile': profile})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def my_clients(request):
    return render(request, 'my_clients.html')  # siz yaratgan HTML fayl

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Booking, Employee
from django.core.serializers import serialize
import json
from django.http import JsonResponse
import calendar
from datetime import datetime, timedelta
from django.shortcuts import render

def calendar_view(request):
    # Hozirgi sana
    today = datetime.today()
    
    # Hozirgi oyning birinchi va oxirgi sanasi
    first_day_of_month = today.replace(day=1)
    last_day_of_month = today.replace(day=calendar.monthrange(today.year, today.month)[1])
    
    # Oydagi barcha kunlarni olish
    days_in_month = calendar.monthrange(today.year, today.month)[1]
    week_days = [calendar.day_name[i] for i in range(7)]  # Dushanbadan yakshanbagacha
    
    # Haftaning birinchi kuni
    first_day_weekday = first_day_of_month.weekday()
    
    # Kalendarni yaratish
    weeks = []
    current_week = [""] * first_day_weekday  # Oydagi ilk kun uchun bo'sh joylar
    
    for day in range(1, days_in_month + 1):
        current_week.append(day)
        
        if len(current_week) == 7:
            weeks.append(current_week)
            current_week = []
    
    if current_week:  # Agar oxirgi haftada kamroq kunlar bo'lsa
        weeks.append(current_week)
    
    context = {
        'weeks': weeks,
        'week_days': week_days,
        'today': today,
        'month': today.month,
        'year': today.year,
        'first_day_of_month': first_day_of_month,
        'last_day_of_month': last_day_of_month,
    }

    return render(request, 'calendar.html', context)

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Customer

@login_required
def my_clients_view(request):
    clients = Customer.objects.filter(referred_by__user=request.user)
    return render(request, 'my_clients.html', {'clients': clients})

import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

BOTPRESS_API_URL = "http://localhost:3000/api/v1/bots/your-bot-id/converse"

@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message')
        session_id = data.get('session_id', 'default_session')  # session_id berilishi mumkin

        payload = {
            "type": "text",
            "text": user_message,
            "sessionId": session_id
        }

        
        response = requests.post(BOTPRESS_API_URL, json=payload)
        
        if response.status_code == 200:
            bot_response = response.json()
            
            return JsonResponse(bot_response)
        else:
            return JsonResponse({'error': 'Botpress API error'}, status=500)

    return JsonResponse({'error': 'Invalid method'}, status=405)

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from django.shortcuts import render
from django.http import HttpResponse
from io import BytesIO
import base64
import pandas as pd
from sklearn.cluster import KMeans
from django.shortcuts import render
from .models import Booking, Service

def customer_segments(request):
   
    bookings = Booking.objects.all().values(
        'customer_id',
        'price_type',
        'final_price',
        'discount_applied'
    )

   
    df = pd.DataFrame(bookings)

    if df.empty:
        return render(request, 'segments.html', {'message': 'Ma\'lumotlar mavjud emas'})

    
    df['price_type_num'] = df['price_type'].map({'Oddiy': 0, 'Premium': 1, 'Boshqa': 2})
    df['discount_applied_num'] = df['discount_applied'].map({'yo\'q': 0, 'ha': 1})

    
    grouped = df.groupby('customer_id').agg({
        'price_type_num': 'mean',
        'final_price': 'mean',
        'discount_applied_num': 'mean'
    }).reset_index()

    
    X = grouped[['price_type_num', 'final_price', 'discount_applied_num']]
    kmeans = KMeans(n_clusters=3, random_state=0)
    grouped['cluster'] = kmeans.fit_predict(X)

    # 6. Natijalarni grafik va jadval bilan chiqaramiz
    context = {
        'segments': grouped.to_dict(orient='records'),
        'cluster_centers': kmeans.cluster_centers_.tolist()
    }

    return render(request, 'segments.html', context)

def home(request):
    services = Service.objects.all()
    return render(request, 'home.html', {'services': services})
import random
import string

def generate_unique_referral_code():
    from .models import Customer
    
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    while Customer.objects.filter(referral_code=code).exists():
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))  # Yangilash
    return code

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Customer

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        phone = request.POST['phone']
        address = request.POST['address']
        referral_code = request.POST.get('referral')

        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Bu username allaqachon mavjud.")
            return redirect('register')

        
        user = User.objects.create_user(username=username, password=password)
        customer = Customer.objects.create(user=user, phone=phone, address=address, discount=0, referral_code=generate_unique_referral_code())

        
        if referral_code:
            try:
                referred_by_customer = Customer.objects.get(referral_code=referral_code)
                customer.referred_by = referred_by_customer
                customer.save()

                apply_discount(customer)  # 👉 CHEGIRMA hisoblash
            except Customer.DoesNotExist:
                pass


        return redirect('profile')  # Success page

    return render(request, 'register.html')

################
from django.shortcuts import render
from .models import Customer

def register_customer(request):
    if request.method == 'POST':
        username = request.POST['username']
        phone = request.POST['phone']
        address = request.POST['address']
        referral_code = request.POST.get('referral_code')

        new_customer = Customer.objects.create(
            user=request.user,
            phone=phone,
            address=address,
            referral_code=referral_code
        )

        # Referral kodi bo'lsa, tekshirish va unga chegirma qo'llash
        if referral_code:
            try:
                referred_user = Customer.objects.get(referral_code=referral_code)
                new_customer.referred_by = referred_user
                new_customer.save()

                apply_discount(new_customer)  # 👉 CHEGIRMA hisoblash
            except Customer.DoesNotExist:
                pass

        else:
            new_customer.discount = 0
            new_customer.save()

        return render(request, 'profile.html', {'customer': new_customer})


def apply_discount(new_customer):
    # Yangi mijozga 5% chegirma beriladi
    new_customer.discount = 5
    new_customer.save()

    # Agar tavsiya bilan kelgan bo‘lsa
    if new_customer.referred_by:
        referred_user = new_customer.referred_by

        # U orqali nechta foydalanuvchi kelganini aniqlaymiz
        referral_count = Customer.objects.filter(referred_by=referred_user).count()

        # Har biri uchun 10%, lekin maksimum 5 ta foydalanuvchigacha, maksimal 50%
        if referral_count <= 5:
            referred_user.discount = referral_count * 10
            if referred_user.discount > 50:
                referred_user.discount = 50
            referred_user.save()


################
from django.shortcuts import render, redirect
from .models import Customer
from .forms import ProfileForm  # If you have a form for editing the profile

def edit_profile(request):
    customer = Customer.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to profile page after saving
    else:
        form = ProfileForm(instance=customer)
    return render(request, 'edit_profile.html', {'form': form})


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Customer

@login_required
def profile(request):
    customer = Customer.objects.get(user=request.user)
    referrals = Customer.objects.filter(referred_by=customer)
    return render(request, 'profile.html', {
        'customer': customer,
        'referrals': referrals
    })


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Login yoki parol noto‘g‘ri!')
    return render(request, 'login.html')

# Chiqish
def logout_view(request):
    logout(request)
    return redirect('home')

from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Service, Employee, Customer, Booking
from decimal import Decimal
from datetime import datetime, timedelta
from .tasks import send_booking_reminder
def booking_view(request):
    if request.user.is_anonymous:
        return render(request, 'please_login.html')  # foydalanuvchi login qilmagan bo‘lsa

    if request.method == 'POST':
        print("POST so'rovi yuborildi")
        service_id = request.POST['service_id']
        employee_id = request.POST['employee_id']
        date = request.POST['date']
        time = request.POST['time']
        booking_date = datetime.strptime(date, "%Y-%m-%d").date()
        booking_time = datetime.strptime(time, "%H:%M").time()
        service = Service.objects.get(id=service_id)
        employee = Employee.objects.get(id=employee_id)
        customer = Customer.objects.get(user=request.user)

        # Xodimning bandligini tekshirish
        bookings = Booking.objects.filter(employee=employee, date=date, time=time)
        if bookings.exists():
            # Band bo'lgan vaqtlar bor bo'lsa, xabar chiqarish
            available_times = get_available_times(employee, date)  # Band bo'lmagan vaqtlar
            if not available_times:  # Agar band bo'lmagan vaqtlar yo'q bo'lsa
                message = "Vaqt tanlash mumkin emas, iltimos boshqa sanani tanlang."
            else:
                message = 'Ushbu vaqt band. Iltimos, boshqa vaqtni tanlang.'

            return render(request, 'booking.html', {
                'services': Service.objects.all(),
                'employees': Employee.objects.all(),
                'available_times': available_times,  # available_times ro'yxatini yuborish
                'message': message,  # Tanlangan xabarni yuborish
                'selected_service_id': service_id,  # Tanlangan xizmatni qaytarish
                'selected_employee_id': employee_id,  # Tanlangan xodimni qaytarish
                'selected_date': date,  # Tanlangan sanani qaytarish
            })
        

        original_price = service.price
        discount_percent = Decimal(str(customer.discount))
        final_price = original_price - (original_price * discount_percent / Decimal('100'))

        booking = Booking.objects.create(
            customer=customer,
            service=service,
            employee=employee,
            date=booking_date,
            time=booking_time,
            final_price=final_price
        )

        if isinstance(booking.date, str):
            booking_date = datetime.strptime(booking.date, "%Y-%m-%d").date()
        else:
            booking_date = booking.date

        if isinstance(booking.time, str):
            booking_time = datetime.strptime(booking.time, "%H:%M").time()
        else:
            booking_time = booking.time

        reminder_time = datetime.combine(booking_date, booking_time) - timedelta(minutes=30)
        send_booking_reminder.apply_async((booking.id,), eta=reminder_time)

        return redirect('my_bookings')

    else:
        services = Service.objects.all()
        employees = Employee.objects.all()

        selected_employee_id = request.GET.get('employee_id')
        selected_date = request.GET.get('date')

        available_times = None
        if selected_employee_id and selected_date:
            employee = Employee.objects.get(id=selected_employee_id)
            available_times = get_available_times(employee, selected_date)

        return render(request, 'booking.html', {
            'services': services,
            'employees': employees,
            'available_times': available_times,
            'selected_employee_id': selected_employee_id,
            'selected_date': selected_date,
        })

from datetime import time

def get_available_times(employee, date):
    booked_times = Booking.objects.filter(employee=employee, date=date).values_list('time', flat=True)

    all_times = [
        time(9, 0), time(10, 0), time(11, 0), time(12, 0),
        time(13, 0), time(14, 0), time(15, 0), time(16, 0)
    ]

    available_times = [t for t in all_times if t not in booked_times]

    # JavaScript uchun string ko‘rinishga qaytarish
    return [t.strftime('%H:%M') for t in available_times]

from django.http import JsonResponse

def get_times_ajax(request):
    employee_id = request.GET.get('employee_id')
    date = request.GET.get('date')
    if not employee_id or not date:
        return JsonResponse({'available_times': []})
    
    try:
        employee = Employee.objects.get(id=employee_id)
        available_times = get_available_times(employee, date)
        return JsonResponse({'available_times': available_times})
    except Employee.DoesNotExist:
        return JsonResponse({'available_times': []})


def update_customer_discount(customer):
    referrals = Customer.objects.filter(referred_by=customer).count()
    if referrals >= 3:
        customer.discount = 15  # bonus chegirma
        customer.save()

@login_required
def edit_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id, customer__user=request.user)
    services = Service.objects.all()
    employees = Employee.objects.all()

    if request.method == 'POST':
        booking.service_id = request.POST.get('service')
        booking.employee_id = request.POST.get('employee')
        booking.date = request.POST.get('date')
        booking.time = request.POST.get('time')
        booking.save()
        messages.success(request, 'Band qilish o‘zgartirildi!')
        return redirect('my_bookings')

    return render(request, 'edit_booking.html', {
        'booking': booking,
        'services': services,
        'employees': employees
    })

from django.shortcuts import get_object_or_404

@login_required
def delete_booking(request, booking_id):
    
    booking = get_object_or_404(Booking, id=booking_id, customer__user=request.user)
    booking.delete()

    messages.success(request, "Xizmat muvaffaqiyatli o'chirildi!")
    return redirect('my_bookings')

from django.contrib.auth.decorators import login_required

@login_required
def my_bookings_view(request):
    customer, created = Customer.objects.get_or_create(user=request.user)
    bookings = Booking.objects.filter(customer=customer).order_by('-date', '-time')
    return render(request, 'my_bookings.html', {'bookings': bookings})


from .models import Review
from .utils import analyze_sentiment  
@login_required
def review_view(request):
    if request.method == 'POST':
        text = request.POST['text']
        service_id = request.POST['service_id']
        service = Service.objects.get(id=service_id)
        customer = Customer.objects.get(user=request.user)

        sentiment = analyze_sentiment(text)  

        Review.objects.create(
            customer=customer,
            service=service,
            text=text,
            sentiment=sentiment
        )

        return redirect('my_bookings')

    services = Service.objects.all()
    return render(request, 'review.html', {'services': services})

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  # faqat test uchun
from django.db.models import Count
from django.shortcuts import render
from .models import Review
import json
from django.core.serializers.json import DjangoJSONEncoder

@csrf_exempt
def service_analysis(request):
    
    top_positive = Review.objects.filter(sentiment='positive') \
        .values('service__name').annotate(count=Count('id')).order_by('-count')[:5]

    top_negative = Review.objects.filter(sentiment='negative') \
        .values('service__name').annotate(count=Count('id')).order_by('-count')[:5]

    if request.method == 'POST':
        
        return JsonResponse({
            'top_positive': list(top_positive),
            'top_negative': list(top_negative)
        })

    
    return render(request, 'service_analysis.html', {
        'top_positive': top_positive,
        'top_negative': top_negative,
        'top_positive_json': json.dumps(list(top_positive), cls=DjangoJSONEncoder),
        'top_negative_json': json.dumps(list(top_negative), cls=DjangoJSONEncoder)
    })
