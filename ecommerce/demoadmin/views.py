from django.shortcuts import render, HttpResponse, redirect , get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from home.models import *
from django.utils import timezone
# Create your views here.

def adminlogin(request) :
    try:
        if request.method == 'POST':
            username = request.POST.get("username")
            password = request.POST.get("password")
            user_obj = User.objects.filter(username = username)
            if not user_obj.exists():
                messages.info(request,'Account not found!')
                return redirect('/')
            user_obj = authenticate(request,username = username,password = password)
            if user_obj and user_obj.is_superuser: # type: ignore
                login(request , user_obj)
                return redirect('dashboard/')
            
            messages.info(request, 'Invalid Password!')
            return redirect('/')
        return render(request,'customadmin/loginform.html')
    except Exception as e:
        print(e)
       

# admin logout 

def adminlogout(request):
    try:
        logout(request)
        return redirect('/')  #  redirect  after logout.
    except Exception as e:
        print(e)

       
def dashboard(request) :
    count = Orders.objects.filter(complete=False).count() # no of order which is not complete
    total_users = User.objects.count() # total number of user
    user_count = User.objects.filter(is_superuser=False).count() # no of user who are non superuser
    # Get today's date and the previous day's date
    today = timezone.now().date()
    previous_day = today - timezone.timedelta(days=1)

    # Count the number of orders from today and the previous day
    orders_today = Orders.objects.filter(date_added=today).count()
    orders_previous_day = Orders.objects.filter(date_added=previous_day).count()
    
    # Calculate the order growth rate
    if orders_previous_day > 0:
        order_growth_rate = (orders_today - orders_previous_day) / orders_previous_day * 100
    else:
        order_growth_rate = 0
    
    
    context = {'undelivered_orders': count ,
               'total_users':total_users,
               'user':user_count,
               'order_growth_rate': order_growth_rate,
               }
    return render(request, 'customadmin/index.html', context)        

# show the calender
def calender(request):
    return render(request, "customadmin/calender.html")

# show all product

def product(request) :
    global_discount_instance, _ = GlobalDiscount.objects.get_or_create(percentage=10)
    product = Product.objects.all()
    return render(request, "customadmin/products.html", {'product':product, 'global_discount': global_discount_instance})


# show all user  except the superuser

def user(request) :
    # if user is not superuser , then only it shows in the user sections
    users = User.objects.filter(is_superuser=False) 
    return render(request, "customadmin/user.html", {'users':users})


# show all order details

def orders(request) :
    all_orders = Orders.objects.all()

    # Prepare data to pass to the template
    orders_data = []
    for order in all_orders:
        order_data = {
            'order_id': order.order_id,
            'email': order.email,
            'cost': order.amount,
            'payment_status': order.paymentstatus,
            'delivery_status': 'Delivered' if order.complete else 'Pending',  
            'address': order.address1 + " " + order.address2 + " " + order.city + " " + order.state + " " + order.zip_code
        }
        orders_data.append(order_data)

    # Pass the data to the template
    return render(request, "customadmin/orders.html", {'orders_data': orders_data})


# add new customer

def add_customer(request):
    if request.method == 'POST':
        user_name = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        user = User.objects.create_user(username=user_name, password=password, email=email)
        user.save()
        messages.success(request, 'Customer added successfully')
        return redirect('/admin/user')
    else:
        return render(request, 'customadmin/addnewuser.html')
    
# edit user

def edit_customer(request, user_id) :
    # find the user
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        # Update the user's details
        username = request.POST.get('username')
        email = request.POST.get('email')
        if username is not None:
            user.username = username
        if email is not None:
            user.email = email
        user.save()

        messages.success(request, 'Customer updated successfully')
        return redirect('/admin/user')
    else:
        # Render the form with the current user details
        return render(request, 'customadmin/edituser.html', {'user': user})    
    
# delete user 

def delete_customer(request, user_id):
    # Get the User object
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        # Delete the user
        user.delete()

        messages.success(request, 'Customer deleted successfully')
        return redirect('/admin/user')
    else:
        # Render a confirmation page
        return render(request, 'customadmin/confirm_delete.html', {'user': user})  
    
# Add new Product      
def add_product(request) :
    if request.method == 'POST' :
        product_id = request.POST.get('product_id')
        product_name = request.POST.get('product_name')
        category = request.POST.get('category')
        subcategory = request.POST.get('subcategory')
        price = request.POST.get('price')
        desc = request.POST.get('desc')
        image = request.POST.get('image')
        pub_date = request.POST.get('pub_date')
        product = Product.objects.create(
            product_id = product_id,
            product_name = product_name, 
            category = category,  
            subcategory = subcategory,
            price = price,
            desc = desc,
            image = image,
            pub_date = pub_date
        )
        product.save()
        messages.success(request, 'Product added successfully')
        return redirect('/admin/product')
    else :
        return render(request, 'customadmin/addproduct.html')
        
        
        
    
# Update product

def edit_product(request, product_id) :
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST' :
        product_id = request.POST.get('product_id')
        product_name = request.POST.get('product_name')
        category = request.POST.get('category')
        subcategory = request.POST.get('subcategory')
        price = request.POST.get('price')
        desc = request.POST.get('desc')
        image = request.POST.get('image')
        pub_date = request.POST.get('pub_date')
        
        if product_id is not None :
            product.product_id = product_id
        if product_name is not None :
            product.product_name = product_name
        if category is not None :
            product.category = category
        if subcategory is not None :
            product.subcategory = subcategory
        if price is not None :
            product.price = price
        if desc is not None :
            product.desc = desc    
        if image is not None :
            product.image = image      
        if pub_date is not None :
            product.pub_date = pub_date
            
        product.save()
        messages.success(request, 'Product Edited Successfully') 
        return redirect('/admin/product')                                       
            
    else :
        return render(request, 'customadmin/editproduct.html', {'product':product})
    

# delete product

def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    if request.method == 'POST':
        # Delete the user
        product.delete()

        messages.success(request, 'Product deleted successfully')
        return redirect('/admin/product')
    else:
        # Render a confirmation page
        return render(request, 'customadmin/confirm_delete_product.html', {'product': product})  
    
    