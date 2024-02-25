from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib import messages 
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from app.models import Customer 

# Create your views here.
@csrf_protect
@login_required(login_url='loginPage')

# Create your views here.
def hello_django(request):
    user_profile = request.user
    user_username = user_profile.username
    user_email = user_profile.email
    print("User:", user_profile)
    print("Username:", user_username)
    print("Email:", user_email)

    try:
        customers = Customer.objects.all()
    except Customer.DoesNotExist:
        customers = None

    context = {
        'user_username': user_username,
        'user_email': user_email,  
        'customers': customers  
    }
    
    return render(request, "index.html", context)

def signUp(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and conform password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('loginPage')
        



    return render (request,'register.html')
     


def loginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login2.html')

def LogoutPage(request):
     logout(request)
     return redirect('loginPage')
    #return render (request,'login2.html')

def profile(request):
    user_profile = request.user
    user_userid =  user_profile.id
    user_username = user_profile.username
    user_email = user_profile.email
    user_fname = user_profile.first_name
    user_lname = user_profile.last_name
    print("User:", user_profile)
    print("id:",user_userid)
    print("Username:", user_username)
    print("Email:", user_email)
    print("Fname:", user_fname)
    print("Lname:", user_lname)
  
    context = {
        'user_username': user_username,
        'user_email': user_email,
        'user_userid': user_userid,
        'user_fname': user_fname,
        'user_lname': user_lname,
        }
    
    return render(request, "profile1.html", context)

def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        user.first_name = request.POST.get('firstname', user.first_name)
        user.last_name = request.POST.get('lastname', user.last_name)
        user.save()
        return redirect('profile1')  # Redirect to the user's profile page after editing

    return render(request, 'editProfile.html', {'user': user})

def order_section(request):
    try:
        customers = Customer.objects.all()
    except Customer.DoesNotExist:
        customers = None
    return render(request, "order.html", {'customers': customers})

def order_details(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    context = {
        'customer': customer,
    }

    return render(request, 'order_details.html', context)
'''
def order_details(request):
    try:
        customers = Customer.objects.all()
    except Customer.DoesNotExist:
        customers = None

    context = {  
        'customers': customers  
    }
    return render(request,"order_details.html",context)
    '''

# views.py

from django.http import JsonResponse

def mark_as_delivered(request, customer_id):
    # Logic to remove the entry from the database
    try:
        # Assuming you have an Order model with an ID field
        customer = get_object_or_404(Customer, id=customer_id)
        customer.delete()
        return JsonResponse({'message': 'Order marked as delivered'}, status=200)
    except Customer.DoesNotExist:
        return JsonResponse({'message': 'Order not found'}, status=404)
    except Exception as e:
        return JsonResponse({'message': f'Error: {e}'}, status=500)
    