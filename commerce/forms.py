from django import forms 

from .models import Payment

class PaymentInitForm(forms.ModelForm):
    amount = forms.CharField(
    widget=forms.TextInput(attrs={'readonly':'readonly'})
)
    product_name = forms.CharField(
    widget=forms.TextInput(attrs={'readonly':'readonly'})
)
    class Meta:
        model = Payment
        fields = ['name','email','phone','product_name','quantity','amount','address']