from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile, Booking, Booking_managed
from django.utils import timezone
from django.core.mail import send_mail
from nuzzaci.settings import EMAIL_HOST_USER
from django.conf import settings

from datetime import datetime
# Create your views here.
def therest(request):
    return render(request, 'therest/index.html')

def aboutview(request):
    return render(request, 'therest/about.html')

def bookview(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            posti = request.POST['posti']
            data = request.POST['data']
            ora = request.POST['ora']
            datetime_obj = datetime.strptime(data, "%Y-%m-%d")
            new_date=datetime_obj.strftime("%d %b, %Y")
            user = User.objects.get(username=request.user.username)
            new_booking = Booking(number=posti, data=data, ora=ora, client=user.userprofile )
            new_booking.save()
            message = f'''Nome: {request.user.userprofile.name}
Giorno: {new_date}
Ora:  {ora}
Posti: {posti}
Vai sul sito per visualizzarla e gestirla.

Ristorante TheRest
            '''
            obj=request.user.userprofile.name+" ti ha appena inviato una richiesta di prenotazione"
            send_mail(
                obj,
                message,
                EMAIL_HOST_USER,
                ["nuzzacigianluca@itis-molinari.eu"],
                fail_silently=False,
            )
            message_to_client = f'''Giorno: {new_date}
Ora:  {ora}
Posti: {posti}
Vai sul sito per visualizzarla. Riceverai la conferma a questo indirizzo.

A presto,

Ristorante TheRest
            '''
            obj_to_client="Hai appena effettuato una richiesta di prenotazione"
            send_mail(
                obj_to_client,
                message_to_client,
                EMAIL_HOST_USER,
                [request.user.email],
                fail_silently=False,
            )
            return redirect('book')
        else:
            posti = request.POST['posti']
            data = request.POST['data']
            datetime_obj = datetime.strptime(data, "%Y-%m-%d")
            new_date=datetime_obj.strftime("%d %b, %Y")
            ora = request.POST['ora']
            nome = request.POST['inputNome']
            email = request.POST['email']
            if User.objects.filter(username=nome).exists():
                if User.objects.get(username=nome).password:
                    messages.error(request, 'Sei già registrato, accedi per prenotare o utilizza un altro nome')
                    return redirect('book')
                else:
                    user = User.objects.get(username=nome)
                    if email != user.email:
                        user.email=email
                        user.save()
                    new_booking = Booking(number=posti, data=data, ora=ora, client=user.userprofile )
                    new_booking.save()
            else:
                user1 = User.objects.create_user(username=nome, email=email)
                new_userprofile=UserProfile(user=user1,name=nome)
                new_userprofile.save()
                new_booking = Booking(number=posti, data=data, ora=ora, client=new_userprofile )
                new_booking.save()
                messages.success(request, 'La tua prenotazione è stata inviata con successo!')

            message = f'''Nome: {nome}
Giorno: {new_date}
Ora:  {ora}
Posti: {posti}
Vai sul sito per visualizzarla e gestirla.

Ristorante TheRest
            '''
            obj=nome+" ti ha appena inviato una richiesta di prenotazione"
            send_mail(
                obj,
                message,
                EMAIL_HOST_USER,
                ["nuzzacigianluca@itis-molinari.eu"],
                fail_silently=False,
            )
            message_to_client = f'''Nome: {nome}  
Giorno: {new_date}
Ora:  {ora}
Posti: {posti}
Riceverai la conferma solo a questo indirizzo.

A presto,

Ristorante TheRest
            '''
            obj_to_client="Hai appena effettuato una richiesta di prenotazione"
            send_mail(
                obj_to_client,
                message_to_client,
                EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return redirect('book')
    return render(request, 'therest/book.html', {
        'dateToday': datetime.today().strftime('%Y-%m-%d')
    })

def loginview(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('login')
    else:
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return render(request, 'therest/login.html')

def manageview(request):
    
    if request.method=='POST':
        if 'confirm' in request.POST:
            confirm = request.POST['confirm']
            idBooking = confirm.split('_')[1]
            book = Booking.objects.get(id=idBooking)
            datetime_obj = datetime.strptime(book.data, "%Y-%m-%d")
            new_date=datetime_obj.strftime("%d %b, %Y")
            managing = Booking_managed(id_booking=book, id_user=book.client, state=True)
            managing.save()
            user=book.client.user
            message_to_client = f'''La tua richiesta di prenotazione è stata accettata.
Promemoria prenotazione:
Data: {new_date}
Ora: {book.ora}
Posti: {book.number}

A presto,

Ristorante TheRest
            '''
            obj_to_client="La tua prenotazione e' stata accettata"
            send_mail(
                obj_to_client,
                message_to_client,
                EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
        if 'refuse' in request.POST:
            refuse = request.POST['refuse']
            idBooking = refuse.split('_')[1]
            book = Booking.objects.get(id=idBooking)
            datetime_obj = datetime.strptime(book.data, "%Y-%m-%d")
            new_date=datetime_obj.strftime("%d %b, %Y")
            managing = Booking_managed(id_booking=book, id_user=book.client, state=False)
            managing.save()
            user=book.client.user
            message_to_client = f'''La tua richiesta di prenotazione è stata rifiutata.
Prenotazione rifiutata:
Data: {new_date}
Ora: {book.ora}
Posti: {book.number}

A presto,

Ristorante TheRest
            '''
            obj_to_client="La tua prenotazione e' stata rifiutata"
            send_mail(
                obj_to_client,
                message_to_client,
                EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
        return redirect('manage')
    list = []
    today = timezone.now().date()
    bookings_to_delete = Booking.objects.all()
    for booking in bookings_to_delete:
        booking_date = datetime.strptime(booking.data, "%Y-%m-%d").date()
        if booking_date < today:
            booking.delete()
    listBookings = Booking.objects.all().order_by('data', 'ora').values()
    bookings_to_check = Booking.objects.all().order_by('data', 'ora').values()
    for booking in bookings_to_check:
        if not Booking_managed.objects.filter(id_booking=booking['id']).exists():
            list.append(booking)
    for i in range(len(list)):
        user = UserProfile.objects.get(id=list[i]['client_id'])
        list[i]['client_name']=user.name
        datetime_obj = datetime.strptime(list[i]['data'], "%Y-%m-%d")
        new_date=datetime_obj.strftime("%d %b, %Y")
        list[i]['data']=new_date
    
    return render(request, 'therest/manage.html', {
        'bookings':list,
    })

def registrationview(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        name=request.POST['name']
        password=request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Sei già registrato, accedi per prenotare o utilizza un altro username')
            return redirect('registration')
        else:
            User.objects.create_user(username=username, email=email, password=password)
            user = authenticate(username=username, password=password)
            UserProfile.objects.create(user=user, role='Client', name=name)
            login(request, user)
            message_to_client = f'''Benvenuto in TheRest.
Le prossime comunicazioni le riceverai a questo indirizzo.

A presto,

Ristorante TheRest

            '''
            obj_to_client="Registrazione effettuata con successo"
            send_mail(
                obj_to_client,
                message_to_client,
                EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            return redirect('home')
    else:
        return render(request, 'therest/registration.html')
def logoutview(request):
    logout(request)
    return render(request, 'therest/login.html')

def mybookingviews(request):
    user = request.user.userprofile
    bookings = Booking.objects.filter(client=user).order_by('data', 'ora').values()
    for i in range(len(bookings)):
        bookings_managed=Booking_managed.objects.filter(id_booking=bookings[i]['id']).values()
        if bookings_managed:
            bookings[i]['state']=bookings_managed[0]['state']
        else:
            bookings[i]['state']='In attesa'
    for element in bookings:
        if element['state']==True:
            element['state']='Accettato'
        elif element['state']==False:
            element['state']='Rifiutato'
        else:
            element['state']='In attesa'
        datetime_obj = datetime.strptime(element['data'], "%Y-%m-%d")
        new_date=datetime_obj.strftime("%d %b, %Y")
        element['data']=new_date
            
            
        

        
    return render(request, 'therest/mybookings.html',{
        'myBookings': bookings
    })

def managedbookingviews(request):
    today = timezone.now().date()
    bookings_to_delete = Booking.objects.all()
    for booking in bookings_to_delete:
        booking_date = datetime.strptime(booking.data, "%Y-%m-%d").date()
        if booking_date < today:
            booking.delete()
 
    list=[]
    bookings_managed=Booking_managed.objects.filter(state=True).values()
    for booking in bookings_managed:
        all_booking = Booking.objects.filter(id=booking['id_booking_id']).values()
        datetime_obj = datetime.strptime(all_booking[0]['data'], "%Y-%m-%d")
        new_date=datetime_obj.strftime("%d %b, %Y")
        booking['data']=new_date
        booking['ora']=all_booking[0]['ora']
        booking['number']=all_booking[0]['number']
        user = UserProfile.objects.get(id=booking['id_user_id'])
        booking['client_name']=user.name


    return render(request,'therest/managed_bookings.html', {
        'bookings':bookings_managed
    })

#manager
#nuzzaci1
