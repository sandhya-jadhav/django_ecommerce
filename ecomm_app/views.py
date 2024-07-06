from django.shortcuts import render,HttpResponse,redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
# from ecomm_app.models import product
from django.shortcuts import render
from .models import product,Cart, Order
from django.db.models import Q
import random
import razorpay
from django.core.mail import send_mail
from django.shortcuts import redirect
# from .models import CartItem

# Create your views here.
def home1(request):
    context={}
    return render(request, 'home1.html',context)

def about(request):
    # return HttpResponse("This is about page")
    context={}
    return render(request,'about.html',context)


def contact(request):
    context={}
    return render(request,'contact.html',context)
    #return HttpResponse("This is contact page")

#---------estore project-------------
def home(request):
    context={}
    p=product.objects.filter(is_active=True) #5 objects
    print(p)
    context['products']=p
    return render(request,'index.html',context)

def product_details(request,pid):
    #print("id of the product:",pid)
    p=product.objects.filter(id=pid)
    print(p)
    context={}
    context['products']=p
    return render(request,'product_details.html',context)

def register(request):
    if request.method=='POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        context={}
        if uname=="" or upass=="" or ucpass=="":#F or T or F=>T
            context['errmsg']="Fields cannot be empty"
            return render(request,'register.html',context)
        elif upass!=ucpass: 
            context['errmsg']="Password and confirm password didn't match"
            return render(request,'register.html',context)
        else:
            try:
                u=User.objects.create(password=upass,username=uname,email=uname)
                u.set_password(upass)
                u.save()
                context['success']="User Created Successfully, please login"
                return render(request,'register.html',context)
            except Exception:
                context['errmsg']="User with same username already Exist"
                return render(request,'register.html',context)
    else:
        return render(request,'register.html')

def user_login(request):
    if request.method=='POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        #print(uname,"-",upass)
        context={}
        if uname=="" or upass=="":
            context['errmsg']="Fields can not be empty"
            return render(request,'login.html',context)
        else:
            u=authenticate(username=uname,password=upass)
            #print(u)  #user object-thirduser@gmail.com
            #print(u.is_superuser,"-",u.password)
            if u is not None:   #None != None =>F
                login(request,u)  #session start
                return redirect('/')    #home page
            else:
                context['errmsg']="Invalid Username and Password"
                return render(request,'login.html',context)
    else:
        return render(request,'login.html')
    
def user_logout(request):
    logout(request)
    return redirect('/')

def catfilter(request,cv):
    q1=Q(is_active=True)
    q2=Q(cat=cv)
    p=product.objects.filter(q1&q2)
    print(p)
    context={}
    context['products']=p
    return render(request,'index.html',context)



def sort(request,sv):  #sv='0'  
    if sv=='0':
        col='price'
    else:
        col='-price'
    p=product.objects.filter(is_active=True).order_by(col)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def range(request):
    min=request.GET['min']
    max=request.GET['max']
    q1=Q(price__gte=min)   #500
    q2=Q(price__lte=max)   #2000
    q3=Q(is_active=True)
    p=product.objects.filter(q1&q2&q3)
    context={}
    context['products']=p
    return render(request,'index.html',context)
    #return HttpResponse("values fetched")

def addtocart(request,pid):
    if request.user.is_authenticated:
        userid=request.user.id
        u=User.objects.filter(id=userid)
        p=product.objects.filter(id=pid)
        #check product exist or not
        q1=Q(uid=u[0])   #6th object
        q2=Q(pid=p[0])   # 7th objects
        c=Cart.objects.filter(q1&q2)   #[<object 9>]
        n=len(c)
        context={}
        context['products']=p
        if n==1:
            context['errmsg']="Product already exist!!"
        else:
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            context['success']="Product Added Successfully to cart!!"
        return render(request,'product_details.html',context)
            # return HttpResponse("Product added in cart")
    else:
        return redirect('/login')
    
def viewcart(request):
    #uid=request.user.id
    c=Cart.objects.filter(uid=request.user.id)  #seconduser
    np=len(c)
    # print(np)
    s=0
    for x in c:
        # print(x)
        # print(x.pid.price)
        s=s+x.pid.price*x.qty   #s=3500*2 + 660
    # print(s)
    context={}
    context['data']=c
    context['total']=s
    context['n']=np
    return render(request,'cart.html',context)

def remove(request,cid):  #cid=1
    c=Cart.objects.filter(id=cid)  #id=1
    c.delete()
    return redirect('/viewcart')

# def remove_from_cart(request, cid):
#     if request.method == 'POST':
#         # Remove the product from the user's cart
#         CartItem.objects.filter(id=cid, user=request.user).delete()
#         # Redirect back to the cart page
#         return redirect('/viewcart')
















def updateqty(request,qv,cid):  
    c=Cart.objects.filter(id=cid)
    # print(c)
    # print(c[0])
    # print(c[0].qty)
    if qv=='1':   #'0'=='1'
        t=c[0].qty+1
        c.update(qty=t)      #update operation
    else:
        if c[0].qty>1:   #1 > 1 => F
            t=c[0].qty-1
            c.update(qty=t)      
    #return HttpResponse("Quantity")
    return redirect('/viewcart')

def placeorder(request):
    userid=request.user.id     #2
    c=Cart.objects.filter(uid=userid)
    print(c)
    oid=random.randrange(1000,9999)
    print(oid)
    for x in c:
        o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()         # order object
        x.delete()        # cart object
    # return HttpResponse("In placeorder")
    orders=Order.objects.filter(uid=request.user.id)
    np=len(orders)
    s=0
    for x in orders:
        s=s + x.pid.price*x.qty
    context={}
    context['data']=orders
    context['n']=np
    context['total']=s
    return render(request,'placeorder.html',context)

def makepayment(request):
    uemail=request.user.email
    print(uemail)
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    np=len(orders)
    for x in orders:
        s=s + x.pid.price*x.qty
        oid=x.order_id               #7600
    
    client = razorpay.Client(auth=("rzp_test_sW7nsZ2nLRroAg", "mZXVODETqD0ehEG70vsEoQz2"))
    data = { "amount": s*100, "currency": "INR", "receipt": oid }  #548000paise => 5480
    payment = client.order.create(data=data)
    # print(payment)
    context={}
    context['data']=payment
    context['uemail']=uemail
    #return HttpResponse("success")
    return render(request,'pay.html',context)

def sendusermail(request,uemail):    #uemail=thirduser
    msg="order details are :"
    context={}
    
    send_mail(
        "Ekart-order place successfully! ",
        msg,
        "sindhusanshya22@gmail.com",
        [uemail],               #user mail id
        fail_silently=False,
    )
    return render(request,'sendemail.html',context)


    # return HttpResponse("Mail send Successfully to user")
