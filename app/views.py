from django.shortcuts import render,redirect
from django.views import View
from .models import Customer,Product,Cart,OrderPlaced
from .forms import CustomerRegistrationForm,CustomerProfileForm,ContactForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
#from django.http import HttpResponse
from django.http import FileResponse
from reportlab.pdfgen import canvas
#import razorpay
from django.conf import settings


class ProductView(View):
 def get(self,request):
  totalitem = 0
  men = Product.objects.filter(category= 'M')
  women = Product.objects.filter(category= 'W')
  kids = Product.objects.filter(category= 'K')
  if request.user.is_authenticated:
   totalitem = len(Cart.objects.filter(user=request.user))
  return render(request, 'app/home.html', 
                {'men':men,'women':women,'kids':kids, 'totalitem':totalitem})

class ProductDetailView(View):
 def get(self, request, pk):
  totalitem = 0
  product = Product.objects.get(pk=pk)
  item_already_in_cart = False
  if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
    item_already_in_cart =Cart.objects.filter(Q
                                              (product=product.id) & Q(user=request.user)).exists() 
  return render(request, 'app/productdetail.html',
                {'product':product,'item_already_in_cart':item_already_in_cart,'totalitem':totalitem})

@login_required
def add_to_cart(request):
 user = request.user
 product_id = request.GET.get('prod_id')
 product = Product.objects.get(id=product_id)
 Cart(user=user,product=product).save()
 return redirect('/cart')

@login_required
def show_cart(request):
 totalitem = 0
 if request.user.is_authenticated:
  totalitem = len(Cart.objects.filter(user=request.user))
  user = request.user
  cart = Cart.objects.filter(user=user)
  print(cart)
  amount = 0.0
  shipping_amount = 70.0
  total_amount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user == user]
  if cart_product:
   for p in cart_product:
    tempamount = (p.quantity * p.product.discounted_price)
    amount += tempamount 
    totalamount = amount + shipping_amount
   return render(request, 'app/addtocart.html',
                {'carts':cart,'totalamount':totalamount, 'amount':amount,'totalitem':totalitem})
  else:
   return render(request, 'app/emptycart.html',{'totalitem':totalitem})
 

def plus_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.quantity+=1
  c.save()
  amount = 0.0
  shipping_amount = 70.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
   tempamount = (p.quantity * p.product.discounted_price)
   amount += tempamount 

  data = {
    'quantity': c.quantity,
    'amount': amount,
    'totalamount': amount + shipping_amount
   }
  return JsonResponse(data)
 
def minus_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.quantity-=1
  c.save()
  amount = 0.0
  shipping_amount = 70.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
   tempamount = (p.quantity * p.product.discounted_price)
   amount += tempamount 

  data = {
    'quantity': c.quantity,
    'amount': amount,
    'totalamount': amount + shipping_amount
   }
  return JsonResponse(data)

def remove_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.delete()
  amount = 0.0
  shipping_amount = 70.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
   tempamount = (p.quantity * p.product.discounted_price)
   amount += tempamount 

  data = {
    'amount': amount,
    'totalamount':amount + shipping_amount
   }
  return JsonResponse(data)

def plus_size(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.size+=1
  c.save()
  data = {
    'size': c.size,
   }
 return JsonResponse(data)

def minus_size(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.size-=1
  c.save()
  data = {
    'size': c.size,
   }
 return JsonResponse(data)

def buy_now(request):
 return render(request, 'app/buynow.html')

@login_required 
def address(request):
 totalitem = 0
 if request.user.is_authenticated:
   totalitem = len(Cart.objects.filter(user=request.user))
   add = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html',{'add':add,'active':'btn-primary','totalitem':totalitem})

@login_required
def orders(request):
 totalitem = 0
 if request.user.is_authenticated:
   user = request.user
   add = Customer.objects.filter(user=user)
   totalitem = len(Cart.objects.filter(user=request.user))
   op = OrderPlaced.objects.filter(user=request.user)
   cart_items = Cart.objects.filter(user=user)
   amount = 0.0
   shipping_amount = 70.0
   totalamount = 0.0
   cart_product = [p for p in Cart.objects.all() if p.user == request.user]
   if cart_product:
    for p in cart_product:
     tempamount = (p.quantity * p.product.discounted_price)
     amount += tempamount 
     totalamount = amount + shipping_amount
   #op = [p for p in OrderPlaced.objects.all() if p.user == request.user]
 return render(request, 'app/orders.html', {'order_placed':op, 'add':add,'totalitem':totalitem,
                                             'totalamount':totalamount,'cart_items':cart_items})
def men(request, data=None):
 totalitem = 0
 if request.user.is_authenticated:
  totalitem = len(Cart.objects.filter(user=request.user))
  if data == None:
   mens = Product.objects.filter(category='M')
  elif data == 'Formal' or data == 'Sports' or data == 'Sandals':
   mens = Product.objects.filter(category='M').filter(brand=data)
  elif data == 'Below':
   mens = Product.objects.filter(category='M').filter(discounted_price__lt=500)
  elif data == 'Above':
   mens = Product.objects.filter(category='M').filter(discounted_price__gt=500)
 return render(request, 'app/men.html',{'mens':mens,'totalitem':totalitem})

def women(request, data=None):
 totalitem = 0
 if request.user.is_authenticated:
  totalitem = len(Cart.objects.filter(user=request.user))
  if data == None:
   womens = Product.objects.filter(category='W')
  elif data == 'Ethnic' or data == 'Formal' or data == 'Sports' or data == 'Sandals':
   womens = Product.objects.filter(category='W').filter(brand=data)
  elif data == 'Below':
   womens = Product.objects.filter(category='W').filter(discounted_price__lt=700)
  elif data == 'Above':
   womens = Product.objects.filter(category='W').filter(discounted_price__gt=700) 
 return render(request, 'app/women.html',{'womens':womens,'totalitem':totalitem})

def kid(request, data=None):
 totalitem = 0
 if request.user.is_authenticated:
  totalitem = len(Cart.objects.filter(user=request.user))
  if data == None:
   kids = Product.objects.filter(category='K')
  elif data == 'Formal' or data == 'Sports_Shoes' or data == 'Sandals':
   kids = Product.objects.filter(category='K').filter(brand=data)
  elif data == 'Below':
   kids = Product.objects.filter(category='K').filter(discounted_price__lt=500)
  elif data == 'Above':
   kids = Product.objects.filter(category='K').filter(discounted_price__gt=500)  
 return render(request, 'app/kid.html',{'kids':kids,'totalitem':totalitem})

class CustomerRegistrationView(View):
 def get(self, request):
  form = CustomerRegistrationForm()
  return render(request, 'app/customerregistration.html',{'form':form})
 
 def post(self, request):
  form = CustomerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request, 'Congratulations!! Registered Successfully')
   form.save()
  return render(request, 'app/customerregistration.html',{'form':form})

@login_required
def checkout(request):
 totalitem = 0
 if request.user.is_authenticated:
  totalitem = len(Cart.objects.filter(user=request.user))
  user = request.user
  add = Customer.objects.filter(user=user)
  cart_items = Cart.objects.filter(user=user)
  amount = 0.0
  shipping_amount = 70.0
  totalamount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  if cart_product:
   for p in cart_product:
    tempamount = (p.quantity * p.product.discounted_price)
    amount += tempamount 
    totalamount = amount + shipping_amount
 return render(request, 'app/checkout.html', {'add':add, 'totalamount':totalamount,'cart_items':cart_items,'totalitem':totalitem})


@login_required
def payment_done(request):
 user = request.user
 custid = request.GET.get('custid')
 customer = Customer.objects.get(id=custid)
 cart = Cart.objects.filter(user=user)
 for c in cart:
  OrderPlaced(user=user,customer=customer, product=c.product, quantity=c.quantity, size=c.size).save() 
  c.delete()
 return redirect("orders")



@method_decorator(login_required, name='dispatch')
class ProfileView(View):
 def get(self, request):
  totalitem = 0
  if request.user.is_authenticated:
   totalitem = len(Cart.objects.filter(user=request.user))
   form = CustomerProfileForm()
  return render(request, 'app/profile.html', {'form':form,
                                              'active':'btn-primary','totalitem':totalitem})
 
 def post(self, request):
  totalitem = 0
  if request.user.is_authenticated:
   totalitem = len(Cart.objects.filter(user=request.user))
   form = CustomerProfileForm(request.POST)
   if form.is_valid():
    usr = request.user
    name = form.cleaned_data['name']
    locality = form.cleaned_data['locality']
    city = form.cleaned_data['city']
    state = form.cleaned_data['state']
    zipcode = form.cleaned_data['zipcode']
    reg = Customer(user=usr,name=name,locality=locality,city=city,
                  state=state,zipcode=zipcode)
    reg.save()
    messages.success(request, 'Congratulations!! Profile Updated Successfully')
  return render(request,'app/profile.html',
                {'form':form,'active':'btn-primary','totalitem':totalitem})


def category(request):
 return render(request,'app/category2.html')

def payment(request):
 totalitem = 0
 if request.user.is_authenticated:
   user = request.user
   add = Customer.objects.filter(user=user)
   op = OrderPlaced.objects.filter(user=request.user)
   amount = 0.0
   shipping_amount = 70.0
   totalamount = 0.0
   cart_product = [p for p in Cart.objects.all() if p.user == request.user]
   if cart_product:
    for p in cart_product:
     tempamount = (p.quantity * p.product.discounted_price)
     amount += tempamount 
     totalamount = amount + shipping_amount
   #op = [p for p in OrderPlaced.objects.all() if p.user == request.user]
 return render(request, 'app/paymentnew.html', {'order_placed':op, 'add':add,
                                             'totalamount':totalamount})


class SearchResultsView(ListView):
    model = Product
    template_name = "app/search_results.html"

    def get_queryset(self):  # new
        query = self.request.GET.get("q")
        object_list = Product.objects.filter(
            Q(title__icontains=query) | Q(category__icontains=query) | Q(brand__icontains=query)
            | Q(discounted_price__icontains=query)
        )
        return object_list


@login_required
def contactus(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'app/home.html')
    form = ContactForm()
    context = {'form': form}
    return render(request, 'app/contactus.html', context)


def aboutus(request):
 return render(request,'app/aboutus.html')


def generate_pdf(request):
    response = FileResponse(generate_pdf_file(), 
                            as_attachment=True, 
                            filename='efvs_bill.pdf')
    return response
 
 
def generate_pdf_file():
    from io import BytesIO
 
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
 
    # Create a PDF document
    dtlss = Customer.objects.all()
    dtls = Cart.objects.all()
    p.drawString(100, 750, "Bill Detail")

    y = 700
    for dtll in dtlss:
        p.drawString(100, y, f"Name: {dtll.name}")
        p.drawString(100, y - 20, f"Address: {dtll.locality},{dtll.city},{dtll.state} - {dtll.zipcode}")
        y -= 40

    for dtl in dtls:
        p.drawString(100, y - 40, f"Product: {dtl.product.title}")
        p.drawString(100, y - 60, f"Quantity: {dtl.quantity}")
        p.drawString(100, y - 80, f"Size: {dtl.size}")
        p.drawString(100, y - 100, f"Price: {dtl.total_cost}")
        y -= 120

    p.showPage()
    p.save()
 
    buffer.seek(0)
    return buffer