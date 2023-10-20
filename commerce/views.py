from django.shortcuts import render, get_object_or_404, redirect

from django.core.exceptions import ObjectDoesNotExist

from commerce.models import *

from django.contrib import messages

from django.urls import reverse

from django.conf import settings

from .forms import PaymentInitForm

import json

import requests

# paystack instance
api_key = settings.PAYSTACK_TEST_SECRET_KEY
url = settings.PAYSTACK_INITIALIZE_PAYMENT_URL

# Create your views here.

def home(request):
    store = Shop.objects.order_by('-created')[:3]
    return render(request, 'client/index.html', {'store':store})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        print(name, email, phone, subject, message)

        data = Contact.objects.create(name=name, email=email, phone=phone, subject=subject, message=message)

        data.save()
        print('Success')
        messages.success(request, 'Your Message was Delivered Successfully')

    return render(request, 'client/contact.html')

def about(request):
    return render(request, 'client/about.html')

def store(request):
    store = Shop.objects.order_by('-created')
    return render(request, 'client/shop.html', {'store':store})

def product_details(request, slug):
    product = get_object_or_404(Shop, slug=slug)
    return render(request, 'client/single-product.html', {'product':product})

# payment processing 

def payment_initiation(request, slug):
    if request.method == 'POST':
        # get form data if POST request
        form = PaymentInitForm(request.POST)
        store_checkout = get_object_or_404(Shop, slug=slug)
        
        # validate form before saving
        if form.is_valid():
            payment = form.save(commit=False)
            payment.amount = store_checkout.product_price
            payment.save()
            # set the payment in the current session
            request.session['payment_id'] = payment.id
            # message alert to confirm payment initiation
            messages.success(request, 'Payment Initiated Successfully.')
            # redirect user for payment completion
            return redirect(reverse('commerce:process'))
    else:
        # render form if GET request
        store_checkout = get_object_or_404(Shop, slug=slug)
        initial_data = {'amount':store_checkout.product_price, 'product_name':store_checkout.product_name}
        form = PaymentInitForm(initial=initial_data)
    return render(request, 'client/payment_init.html', {'form':form},)


def payment_process(request):
    # recall the payment_id we'd set in django session earlier
    payment_id = request.session.get('payment_id', None)
    
    # using the payment_id, get the database object 
    payment = get_object_or_404(Payment, id=payment_id)
    
    #  retrieve product quantity
    quantity = payment.get_quantity()
    # retrieve payment amount
    amount = payment.get_amount()
    
    # retrieve product being paid for 
    product = payment.get_product()
    
    # retrieve customer's details
    phone  = payment.get_phone()
    full_name = payment.get_full_name()
    
    if request.method == 'POST':
        success_url = request.build_absolute_uri(
            reverse('commerce:success'))
        cancel_url = request.build_absolute_uri(
            reverse('commerce:canceled'))
        
        # metadata to pass additional data that 
        # the endpoint doesn't accept naturally.
        metadata = json.dumps({"payment_id":payment_id, "cancel_action":cancel_url})
        
        # Paystack checkout session data
        session_data = {
            'email':payment.email,
            'full_name':full_name,
            'product':product,
            'quantity':quantity,
            'amount':int(amount)*100,
            'phone':phone,
            'callback_url':success_url,
            'metadata':metadata
        }
        
        headers = {"authorization":f"Bearer {api_key}"}
        # API request to paystack server
        
        r = requests.post(url,headers=headers, data=session_data)
        response = r.json()
        if response["status"] == True:
            # redirect to paystack payment form
            try:
                redirect_url = response["data"]["authorization_url"]
                return redirect(redirect_url, code=303)
            except :
                pass
        else:
            return render(request, 'client/process.html', locals())
    else:
        return render(request, 'client/process.html', locals())
    
def payment_success(request):
    # retrieve the payment_id we'd set in the django session earlier 
    payment_id = request.session.get('payment_id', None)
    # using the payment_id, get the database object 
    payment = get_object_or_404(Payment, id=payment_id)
    
    # retrieve the query parameter from the request object
    ref = request.GET.get('reference','')
    # verify transaction endpoint
    url='https://api.paystack.co/transaction/verify/{}'.format(ref)
    
    # set auth header
    headers = {"authorization":f'Bearer {api_key}'}
    r = requests.get(url, headers=headers)
    res = r.json()
    res = res["data"]
    
    # verify status before setting payment_ref
    if res['status'] == "success":
        # update payment reference
        payment.paystack_ref = ref
        payment.paid = True
        payment.save()
        
    return render(request, 'client/success.html')

def payment_canceled(request):
    return render(request, 'client/canceled.html')

