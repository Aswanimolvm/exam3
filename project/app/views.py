from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import User,Product,cart

# Create your views here.
def register(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        username=request.POST['username']
        if User.objects.filter(username=username).exists():
            return render(request,"registration.html",{'message':"username already exists"})
        password=request.POST['password']
        data=User.objects.create(name=name,email=email,username=username,password=password)
        data.save()
        return render(request,"login.html")
    else:
        return render(request,"registration.html")

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        try:
            data=User.objects.get(username=username)
            if data.password==password:
                request.session['id']=data.id
                return redirect(product)
            else:
                return render(request,'login.html',{'message':"Password doesn't match"})
        except Exception:
            return render(request,'login.html',{'message':'Username doesnot exists'})
        
    else:
        return render(request,'login.html')

def product(request):
    data=Product.objects.all()   
    context={
        data:product
    } 
    return render(request,'product.html',context)


def add_to_cart(request, id):
    product = Product.objects.get(id=id)
    
    if 'cart' not in request.session:
        request.session['cart'] = []
    
    cart = request.session['cart']
    
    if id not in cart:
        cart.append(id)
        request.session['cart'] = cart
    
    return redirect('cart_view')


def cart_view(request):
    cart = request.session.get('cart', [])
    products = Product.objects.filter(id__in=cart)
    
    context = {
        'cart_items': products
    }
    return render(request, 'cart.html', context)


def cart_delete(request, id):
    cart = request.session.get('cart', [])
    
    if id in cart:
        cart.remove(id)
        request.session['cart'] = cart
    
    return redirect('cart_view')


