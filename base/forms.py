from django.forms import ModelForm
from .models import Customers, Purchase, Sales

class customerForm(ModelForm):
    class Meta:
        model=Customers
        fields='__all__'

class purchaseForm(ModelForm):
    class Meta:
        model=Purchase
        fields=['payment_method']

class saleForm(ModelForm):
    class Meta:
        model=Sales
        fields=['payment_method']