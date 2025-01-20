from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from ecomapp.models import Product,Cart,Order
from django.db.models import Q
import razorpay
from django.core.mail import send_mail

# Create your views here.
def register(request):
    context={}
    if request.method=='GET':
        return render(request,'register.html')
    else:
        n= request.POST['uname']
        e= request.POST['uemail']
        p= request.POST['upass']
        cp= request.POST['ucpass']

           
        #l=len(p)
        if n=="" or e=="" or p=="" or cp=="":
            print('Fields cannot be empty')
            context['errmsg']='Fields cannot be empty'
        elif p!=cp:
            print('Passsword & Confirm Password not matching')
            context['errmsg']='Passsword & Confirm Password not matching'
        #elif l<8:
        elif len(p)<8:
            print('Password must be greater then 8')
            context['errmsg']='Password must be greater then 8'
        else: 
            try:
                u= User.objects.create(username=n,email=e) 
                u.set_password(p)
                u.save()
                context['success']='User registered successfully..!'
            except Exception:
                context['errmsg']='Users already exists'


        return render(request,'register.html',context)
            
        return HttpResponse('Data Fetched')

def user_login(request):
    context={}  
    if request.method=='GET':
        return render(request,'login.html')
    else:
        n=request.POST['uname']
        p=request.POST['upass']
        # print(n)
        # print(p)
        u=authenticate(username=n,password=p)
        # print(u)
        if u!=None:
            login(request,u)
            return redirect('/product')
        else:
            context['errmsg']='Invalid Credentials'
            return render(request,'login.html',context)

def user_logout(request):
    logout(request)
    return redirect('/product')

def product(request):
    p=Product.objects.filter(is_active=True)
    #print(p)
    context={}
    context['data']=p
    return render(request,'product.html',context)

def catfilter(request,cv):
    #print(cv) 
    q1=Q(cat=cv)
    q2=Q(is_active=True)
    p=Product.objects.filter(q1 & q2)
    #print(p)
    context={}
    context['data']=p
    return render(request,'product.html',context)

def sortfilter(request,sv):
    #print(sv)
    context={}
    if sv=="1":
        p=Product.objects.order_by('-price').filter(is_active=True)
        context['data']=p
    else:
        p=Product.objects.order_by('price').filter(is_active=True)
        context['data']=p
    return render(request,'product.html',context)

def pricefilter(request):
    mn=request.GET['min']
    mx=request.GET['max']
    #print(mn)
    #print(mx)
    q1=Q(price__gte=mn)
    q2=Q(price__lte=mx)
    q3=Q(is_active=True)

    p=Product.objects.filter(q1 &q2&q3)
    #print(p)
    context={}
    context['data']=p
    return render(request,'product.html',context)


def placeorder(request):
    return render(request,'placeorder.html')

def product_detail(request,pid):
    p=Product.objects.filter(id=pid)
    #print(p)
    context={}
    context['data']=p
    return render(request,'product_detail.html',context)

def addtocart(request,pid):
    context={}
    #print(pid)
    if request.user.is_authenticated:
        #print(request.user.id)-->return the id of login user from session table.
        u= User.objects.filter(id=request.user.id)
        #print(u)
        #print(u[0].email)
        p=Product.objects.filter(id=pid)
        q1=Q(uid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1 & q2)
        
        if len(c)==1:
            context['errmsg']='Product already exist'
        else:
            c=Cart.objects.create(pid=p[0],uid=u[0])
            c.save()
            context['success']='Product added successfully'
        
        context['data']=p
        return render(request,'product_detail.html',context)
    else: 
        return redirect('/login')

    return HttpResponse('Add to cart')


def cart(request):
    c=Cart.objects.filter(uid = request.user.id)
    #print(c)
    s=0
    for i in c:
        s=s+i.pid.price*i.qty
    context={}
    context['data']=c
    context['total']=s
    context['n']=len(c)
    return render(request,'cart.html',context)
    
def updateqty(request,x,cid):
    c=Cart.objects.filter(id = cid) 
    #print(c[0].qty)
    q=c[0].qty
    if x=='1':
        q=q+1
    elif q>1:
        q=q-1
    c.update(qty=q)
    return redirect('/cart')

def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/cart')

def placeorder(request):
    c=Cart.objects.filter(uid=request.user.id)
    for i in c:
        a=i.qty*i.pid.price 
        o=Order.objects.create(uid=i.uid,pid=i.pid,qty=i.qty,amt=a)
        o.save()
        i.delete()
        return redirect('/fetchorder')

def fetchorder(request):
    o=Order.objects.filter(uid=request.user.id)
    context={}
    s=0
    for i in o:
        s=s+i.amt
    context['data']=o
    context['total']=s
    context['n']=len(o)
    return render(request,'placeorder.html',context)

def srcfilter(request):
    s=request.GET['search']
    pname=Product.objects.filter(name__icontains=s)
    pdet=Product.objects.filter(pdetails__icontains=s)
    alldata=pname.union(pdet)
    #print(alldata)
    context={}
    if alldata.count()==0:
        context['errmsg']='Product Not Found'

    context['data']=alldata
    return render(request,'product.html',context)

def makepayment(request):
    
    client = razorpay.Client(auth=("rzp_test_Ngcd6dVh7J5Jdl", "N5dYtHIl3feMfr3nFhapWUgj"))
    o=Order.objects.filter(uid=request.user.id)
    s=0
    for i in o:
        s=s+i.amt

    data = { "amount": s*100, "currency": "INR", "receipt": "order_rcptid_11" }
    payment = client.order.create(data=data) 
    #print(payment)
    context={}
    context['payment']=payment

    return render(request,'pay.html',context)

def paymentsuccess(request):
    sub='Order Confirm'
    msg='Payment Successfull'
    frm='bafnabhushan2143@gmail.com'
    u=User.objects.filter(id=request.user.id)
    to=u[0].email
    send_mail(
        sub,
        msg,
        frm,
        [to],
        fail_silently=False
    )
    
    return render(request,'paymentsuccess.html ')