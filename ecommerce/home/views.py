import json
from django.shortcuts import render,redirect, get_object_or_404
from home.models import Contact,Product,OrderUpdate,Orders, CartItem ,Cart, GlobalDiscount
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt





# Create your views here
# sign up 
def signup(request):
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['pass1']
        confirm_password=request.POST['pass2']
        if password!=confirm_password:
            messages.warning(request,"Password is Not Matching")
            return render(request,'signup.html')                   
        try:
            if User.objects.get(username=email):
                # return HttpResponse("email already exist")
                messages.info(request,"Email is Taken")
                return render(request,'signup.html')
        except Exception as identifier:
            pass
        user = User.objects.create_user(email,email,password)
        user.is_active=True
        user.save()
    return render(request,"signup.html")


# sign in
def handlelogin(request):
    if request.method=="POST":

        username=request.POST['email']
        userpassword=request.POST['pass1']
        myuser=authenticate(username=username,password=userpassword)

        if myuser is not None:
            login(request,myuser)
            messages.success(request,"Login Success")
            return redirect('/')

        else:
            messages.error(request,"Invalid Credentials")
            return redirect('/login')

    return render(request,'login.html')  

# logout
def handlelogout(request):
    logout(request)
    messages.info(request,"Logout Success")
    return redirect('/login')

# home page
def index(request):
    products = Product.objects.all()
    global_discount_instance = GlobalDiscount.objects.first()
    cart_items_count = CartItem.objects.filter(cart__user=request.user).count() if request.user.is_authenticated else 0

    return render(request, 'index.html', {
        'products': products,
        'global_discount': global_discount_instance,
        'cart_items_count': cart_items_count
    })

# product page
def product(request) :
    redirect('/')
    
# Add to cart functility
@login_required(login_url='/login')
def add_to_cart(request, product_id):
    product = Product.objects.get(product_id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user) 
    cart_item, created = CartItem.objects.get_or_create(product=product, cart=cart)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    # cart_items_count = CartItem.objects.filter(cart__user=request.user).count()        
    # print(cart_items_count)
    return redirect('/',)

# cart views
@login_required(login_url='/login')
def cart(request) :
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    if not cart_items:
        return redirect('/')
    global_discount_instance = GlobalDiscount.objects.first()
    total_discountprice = sum(item.product.discounted_price * item.quantity for item in cart_items)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'discount_price':total_discountprice, 
        'actual_price':total_price,
        'global_discount':global_discount_instance})

# remove item from cart
@login_required(login_url='/login')
def remove_from_cart(request, product_id):
    product = Product.objects.get(product_id=product_id)
    cart_item = CartItem.objects.get(product=product, cart__user=request.user)
    cart_item.delete()
    return redirect('/cart')


# update qunantity from cart
@login_required(login_url='/login')
def update_quantity(request, product_id):
    if request.method == 'POST':
        change = int(request.POST.get('change'))
        product = Product.objects.get(product_id=product_id)
        cart_item, created = CartItem.objects.get_or_create(product=product, cart__user=request.user)
        new_quantity = max(0, cart_item.quantity + change)  # Ensure quantity is not negative
        cart_item.quantity = new_quantity
        if cart_item.quantity == 0:
            cart_item.delete()
        else:
            cart_item.save()
    return redirect('/cart')

# check out or buy now

@login_required(login_url='/login')
def buy_now(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        # Get the form data
        name = request.POST.get('name')
        email = request.user.email
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')

        # Create a new order with the single product
        items_json = json.dumps(product.product_name)
        order = Orders.objects.create(
            items_json=items_json,
            amount=product.discounted_price,
            name=name,
            email=email,
            address1=address1,
            address2=address2,
            city=city,
            state=state,
            zip_code=zip_code,
            phone=phone,
            complete=False
        )

        messages.success(request, 'Order Placed Successfully') 
        return redirect('/thankyou') 
    else:
        return render(request, 'checkout.html', {'product': product})

@login_required(login_url='/login')
def buy_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    if request.method == 'POST':
        # Get the form data
        name = request.POST.get('name')
        email = request.user.email
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')


        # Check if the cart is empty
        if not cart_items:
            messages.warning(request, "Your cart is empty.")
            return redirect('/')

        # Iterate over the items in the cart
        for item in cart_items:
            # Create a new order for each item
            items_json = json.dumps(item.product.product_name)
            order = Orders.objects.create(
                items_json=items_json,
                amount=item.product.discounted_price * item.quantity,
                name=name,
                email=email,
                address1=address1,
                address2=address2,
                city=city,
                state=state,
                zip_code=zip_code,
                phone=phone,
                complete=False
            )

            # Optionally, create an OrderUpdate for each order
            OrderUpdate.objects.create(
                order_id=order,
                update_desc="Order placed"
            )

            # Remove the item from the cart
            item.delete()

        messages.success(request, 'Order Placed Successfully') 
        return redirect('/thankyou')
    else:
        # Render the form page
        return render(request, 'buycartitem.html',{'cart_items':cart_items})

def thankyou(request) :
    return render(request, "thankyou.html")

def contact(request):
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        desc=request.POST.get("desc")
        pnumber=request.POST.get("pnumber")
        myquery=Contact(name=name,email=email,desc=desc,phonenumber=pnumber)
        myquery.save()
        messages.info(request,"we will get back to you soon..")
        return render(request,"contact.html")


    return render(request,"contact.html")

def about(request):
    return render(request,"about.html")




def handlerequest(request):
    return render(request, 'paymentstatus.html')


def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Login & Try Again")
        return redirect('/login')
    currentuser=request.user.username
    items=Orders.objects.filter(email=currentuser)
    
    # Fetch the related OrderUpdate instances for each order
    status = {item.order_id: OrderUpdate.objects.filter(order_id=item) for item in items}

   
    context ={"items":items, "status":status}
    return render(request,"profile.html",context)




   
def tracker(request) :
    return render(request, 'tracker.html')        


def contactus(request) :
    return render(request, "contactus.html")


