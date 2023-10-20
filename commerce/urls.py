from django.urls import path

from commerce import webhooks as wh

from. import views

app_name = 'commerce'

urlpatterns = [
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
    path('shop', views.store, name='shop'),
    path('product_details/<slug:slug>', views.product_details, name='product_details'),
    path('payment-init/<slug:slug>', views.payment_initiation, name='payment-init'),
    path('process', views.payment_process, name='process'),
    path('success',views.payment_success, name='success'),
    path('canceled', views.payment_canceled,name='canceled'),
    path('webhook', wh.stack_webhook, name='stack-webhook')
]
