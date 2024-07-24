from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login
from .models import (Amenities,Hotel,HotelBooking)

def check_booking(start_date,end_date,uid,room_count): 
    qs = HotelBooking.objects.filter(
        start_date__lte=start_date,
        end_date__gte=end_date,
        hotel__uid = uid
    )
    if len(qs)>room_count:
        return False
    return True
   

def home(request):
    amenities_obj=Amenities.objects.all()
    hotel_obj=Hotel.objects.all()

    sort_by=request.GET.get('sort_by')
    search=request.GET.get('search')
    amenities=request.GET.getlist('amenities')
    if sort_by:
        sort_det=request.GET.get('sort_by')
        if sort_det=='ASC':
            hotel_obj=hotel_obj.order_by('hotel_price')
        elif sort_det=='DSC':
            hotel_obj=hotel_obj.order_by('-hotel_price')
    if search:
        hotel_obj=hotel_obj.filter(hotel_name=search)
    if len(amenities):
        hotel_obj=hotel_obj.filter(amenities__amenity_name__in=amenities)

    context={"amenities_objs":amenities_obj,"hotel_objs":hotel_obj,"sort_by":sort_by}
    return render(request,'home.html',context)
# Create your views here.

def login_page(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user_obj=User.objects.filter(username=username)

        if not user_obj.exists():
            messages.warning(request,"account doesn't exists")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        user_obj=authenticate(username=username,password=password)
        if not user_obj:
          messages.warning(request,"check for id and password")
          return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        login(request,user_obj)
        return redirect('home')
        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request,'login.html')

def regsiter_page(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user_obj=User.objects.filter(username=username)

        if user_obj.exists():
            messages.warning(request,'account already exists')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        user=User.objects.create(username=username) 
        user.set_password(password)
        user.save()
        return redirect('home')
        
    return render(request,'register.html')

def hoteldetail(request,uid):
    hotel_obj = Hotel.objects.get(uid = uid)
    if request.method == 'POST':
        checkin = request.POST.get('checkin')
        checkout= request.POST.get('checkout')
        hotel =Hotel.objects.get(uid = uid)
        if not check_booking(checkin ,checkout  , uid , hotel.room_count):
            messages.warning(request, 'Hotel is already booked in these dates ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        HotelBooking.objects.create(hotel=hotel , user = request.user , start_date=checkin
        , end_date = checkout , booking_type  = 'Pre Paid')
        messages.success(request, 'Your booking has been saved')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    return render(request,'hoteldetail.html',{"hotels_obj":hotel_obj})
