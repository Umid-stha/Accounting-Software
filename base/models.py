
from django.db import models
import datetime

class Products(models.Model):
    ProductName = models.CharField(max_length=50)
    Rate = models.FloatField(default=0)
    costPrice = models.FloatField(default=0)
    Stock = models.FloatField(default=0)
    wc_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.ProductName

class Customers(models.Model):
    Cus_Name = models.CharField(max_length=50, null=True)
    Cus_Number = models.BigIntegerField(default=0, null=True)
    Cus_Purchase = models.FloatField(default=0,null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.Cus_Name or 'Unnamed Customer'

class Suppliers(models.Model):
    Sup_Name = models.CharField(max_length=50, null=True)
    Sup_Number = models.BigIntegerField(default=0, null=True)
    Sup_Purchase = models.FloatField(default=0,null=True)

    def __str__(self):
        return self.Sup_Name
    
class Expense(models.Model):
    purchasedFrom=models.CharField(max_length=200, null=True)
    total=models.FloatField(default=0)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Expense of Rs.{self.total} from {self.purchasedFrom}'

class ExpenseDetails(models.Model):
    name=models.CharField(max_length=200, null=True)
    quantity=models.FloatField(default=1)
    rate=models.FloatField(default=1)
    Amount=models.FloatField(null=True)
    expense=models.ForeignKey(Expense,on_delete=models.CASCADE, null=True, blank=True)

class Sales(models.Model):
    CASH = 'cash'
    ONLINE = 'online'
    CREDIT = 'credit'
    CREDITCOLL ='creditColl'

    PAYMENT_METHOD = [
        (CASH, 'Cash'),
        (ONLINE, 'Online'),
        (CREDIT, 'Credit'),
        (CREDITCOLL, 'creditColl'),
    ]

    Customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    bill_no=models.IntegerField(default=0)
    Discount = models.FloatField(default=0) 
    TotalAmt = models.FloatField(default=0)
    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_METHOD ,
        default=CASH,
    )
    sale_date = models.DateField(default=datetime.date.today)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f'Sale of {self.Customer} - Bill No: {self.bill_no}'
    
    class Meta:
        ordering=['sale_date']
    
class SaleDetails(models.Model):
    Product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True, blank=True)
    Rate = models.FloatField(default=0)
    Quantity = models.FloatField(default=1)
    Sale = models.ForeignKey(Sales, on_delete=models.CASCADE, null=True, blank=True)   

    def __str__(self):
        return f'{self.Product} ({self.Quantity}) in Sale {self.Sale.id}'


class Purchase(models.Model):
    CASH = 'cash'
    ONLINE = 'online'
    CREDIT = 'credit'
    CREDITCOLL ='creditColl'

    PAYMENT_METHOD = [
        (CASH, 'Cash'),
        (ONLINE, 'Online'),
        (CREDIT, 'Credit'),
        (CREDITCOLL, 'creditColl'),
    ]
    Supplier = models.ForeignKey(Suppliers, on_delete=models.CASCADE)
    Discount = models.FloatField(default=0)
    totalAmtPur = models.FloatField(default=0)
    pur_date = models.DateField(default=datetime.date.today)
    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_METHOD ,
        default=CASH,
    )
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f'Purchase of {self.Supplier}'
    
    class Meta:
        ordering=['pur_date']

class PurchaseDetails(models.Model):
    Product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True, blank=True)
    Quantity = models.FloatField(default=1)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, null=True, blank=True) 
    Rate = models.FloatField(default=0)
    sellRate = models.FloatField(default=0)
    def __str__(self):
        return f'{self.Product} ({self.Quantity}) in Sale {self.purchase.id}'