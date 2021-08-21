from ticketing.forms import ShowTimeSearchForm
from django.http.response import HttpResponseForbidden
from django.shortcuts import render,get_object_or_404
from ticketing.models import Movie,Cinema,ShowTime,Ticket
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.

def movie_list(request):
    movies = Movie.objects.all()
    numOfmovies = len(movies)
    context = {
        'movies' : movies,
        'count' : numOfmovies,
    }
    return render(request,'ticketing/movie_list.html',context)

def movie_details(request,movie_id):
    movie = get_object_or_404(Movie,pk=movie_id)
    context = {
        "movie" : movie ,
    }
    return render(request,'ticketing/movie_details.html',context)

def cinema_list(request):
    cinemas = Cinema.objects.all()
    context = {
        'cinemas' : cinemas
    }
    
    return render(request,'ticketing/cinema_list.html',context)

def cinema_details(request,cinema_id):
    cinema = get_object_or_404(Cinema,pk=cinema_id)
    context = {
        "cinema" : cinema,
    }
    return render(request,'ticketing/cinema_details.html',context)

def showtime_list(request):
    search_form = ShowTimeSearchForm(request.GET)
    showtime = ShowTime.objects.all()
    if search_form.is_valid():
        showtime = showtime.filter(movie__name__contains=search_form.cleaned_data['movie_name'])
        if search_form.cleaned_data['sale_open_only']:
            showtime = showtime.filter(status=ShowTime.SALE_OPEN)
        if search_form.cleaned_data['movie_min_length'] is not None:
            showtime = showtime.filter(movie__length__gte=search_form.cleaned_data['movie_min_length'])
        if search_form.cleaned_data['movie_max_length'] is not None:
            showtime = showtime.filter(movie__length__lte=search_form.cleaned_data['movie_max_length'])
        if search_form.cleaned_data['cinema'] is not None:
            showtime = showtime.filter(cinema=search_form.cleaned_data['cinema'])
        min_price,max_price = search_form.get_price_boundries()
        if min_price is not None:
            showtime = showtime.filter(price__gte=min_price)
        if max_price is not None:
            showtime = showtime.filter(price__lt=max_price)
    
    showtime = showtime.order_by('start_time')
    context = {
        "showtimes" : showtime,
        "search_form" : search_form
    }

    return render(request,'ticketing/showtime_list.html',context)

@login_required
def showtime_details(requset,showtime_id):
    showtime = ShowTime.objects.get(pk=showtime_id)
    context = {
        'showtime' : showtime
    }
    if requset.method == 'POST':
        try:
            seat_count =  int(requset.POST['seat_count'])
            assert showtime.status == ShowTime.SALE_OPEN ,'خرید بلیت برای این سانس ممکن نیست.'
            assert showtime.free_seats >= seat_count,'این سانس صندلی کافی صندلی خالی ندارد.'
            total_price = showtime.price * seat_count
            assert requset.user.profile.spend(total_price),'موجودی حساب شما کافی نیست.'
            showtime.reserve_seats(seat_count)
            ticket=Ticket.objects.create(showtime=showtime,customer=requset.user.profile,seat_count=seat_count)    
        except Exception as e:
            context['error'] = str(e)
        else:
            return HttpResponseRedirect(reverse('ticketing:ticket_details',kwargs={'ticket_id':ticket.id}))
    return render(requset,'ticketing/showtime_details.html',context)



@login_required
def ticket_list(request):
    tickets = Ticket.objects.filter(customer=request.user.profile).order_by('-order_time')
    context = {
        'tickets':tickets
    }

    return render(request,'ticketing/ticket_list.html',context)

@login_required
def ticket_details(request,ticket_id):
    ticket = Ticket.objects.get(pk=ticket_id)
    context = {
        'ticket' : ticket
    }
    return render(request,'ticketing/ticket_details.html',context)