from django.shortcuts import render, redirect
from base.models import Products, Customers, SaleDetails, Sales, Suppliers, Purchase, PurchaseDetails, Expense, ExpenseDetails
from django.http import JsonResponse
from django.db.models import Sum, F
from .forms import customerForm, purchaseForm, saleForm
from .filters import saleFilter, purchaseFilter, productFilter, customerFilter, expenseFilter, supplierFilter
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.paginator import Paginator
import helper

wc = helper.wcapi

# Create your views here.
def loginUser(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect to home if already logged in

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if the username exists
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, 'base/login.html')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    context={}
    return render(request, 'base/login.html', context)

@login_required(login_url='login')
def dashboard(request):
    totalSales=Sales.objects.aggregate(totalSales=Sum('TotalAmt'))['totalSales']
    totalPurchase=Purchase.objects.aggregate(totalPurchase=Sum('totalAmtPur'))['totalPurchase']
    totalExpense=Expense.objects.aggregate(total=Sum('total'))['total']
    totalStock=Products.objects.aggregate(totalStock=Sum(F('Stock') * F('costPrice')))['totalStock']
        # Aggregate total quantity sold for each product and order by quantity in descending order
    top_products = SaleDetails.objects.values('Product__ProductName') \
                                      .annotate(total_quantity=Sum('Quantity')) \
                                      .order_by('-total_quantity')[:6]

    sales_data = Sales.objects.values('sale_date__month').annotate(total_sales=Sum('TotalAmt')).order_by('sale_date__month')
    
    # Prepare data for the chart
    months = [sale['sale_date__month'] for sale in sales_data]
    totals = [sale['total_sales'] for sale in sales_data]

    context = {
                'top_products': list(top_products),
                'totalSales':totalSales,
                'totalPurchase':totalPurchase,
                'totalExpense':totalExpense,
                'totalStock':totalStock,
                'months': months,
                'totals': totals,
                }
    return render(request, 'base/dashboard.html',context)

@login_required(login_url='login')
def sales(request):
    products=Products.objects.all()
    customers=Customers.objects.all()
    if request.method == 'POST':
        Customer_Name=request.POST.get('Customer')
        Customer_Number=request.POST.get('CustomerNumber')
        bill=request.POST.get('bill')
        discount=request.POST.get('discount')
        total=request.POST.get('total')
        sale_date=request.POST.get('sale_date')
        payment_method = request.POST.get('payment_method')
        Customer, created =Customers.objects.get_or_create(Cus_Name=Customer_Name,Cus_Number=Customer_Number)
        sales=Sales.objects.create(
            Customer=Customer,
            bill_no=int(bill),
            Discount=float(discount),
            TotalAmt=float(total),
            payment_method=payment_method,
            sale_date=sale_date
        )
        Customer.Cus_Purchase += float(total)
        Product_names=request.POST.getlist('Product')
        quantities=request.POST.getlist('quantity')
        rates=request.POST.getlist('rate')
        for i in range(len(Product_names)):
            product_name=Product_names[i]
            quantity=quantities[i]
            rate=rates[i]
            product=Products.objects.get(ProductName=product_name)

            product.Stock -= float(quantity)

            sale=SaleDetails.objects.create(
                Product=product,
                Rate=rate,
                Quantity=quantity,
                Sale=sales
            )

            data = {
                'manage_stock': True,
                'stock_quantity': product.Stock
            }

            if product.wc_id is not None:
                wc.put(f"products/{product.wc_id}", data).json()

            product.save()
            Customer.save()
        return redirect('sales')

    context={'customers':customers,'products':products}
    return render(request, 'base/sales.html', context)

@login_required(login_url='login')
def get_customer_details(request):
    customer_name = request.GET.get('customer_name')
    if customer_name:
        customers = Customers.objects.filter(Cus_Name=customer_name)
        customer_numbers = list(customers.values_list('Cus_Number', flat=True))
        return JsonResponse({'numbers': customer_numbers})
    return JsonResponse({'numbers': []})

@login_required(login_url='login')
def get_product_details(request):
    product_name = request.GET.get('product_name', None)
    product = Products.objects.filter(ProductName=product_name).first()
    if product:
        data = {
            'stock': product.Stock,
            'rate': product.Rate,
            'wc_id': product.wc_id
        }
    else:
        data = {}
    return JsonResponse(data)

@login_required(login_url='login')
def purchase(request):
    products=Products.objects.all()
    suppliers=Suppliers.objects.all()
    if request.method == 'POST':
        print(request.POST)
        Supplier_Name=request.POST.get('Supplier')
        Supplier_Number=request.POST.get('SupplierNumber')
        discount=request.POST.get('discount')
        total=request.POST.get('total')
        pur_date=request.POST.get('purchase_date')
        payment_method = request.POST.get('payment_method')
        Supplier, created =Suppliers.objects.get_or_create(Sup_Name=Supplier_Name,Sup_Number=Supplier_Number)
        purchase=Purchase.objects.create(
            Supplier=Supplier,
            Discount=float(discount),
            totalAmtPur=float(total),
            payment_method=payment_method,
            pur_date=pur_date
        )
        Supplier.Sup_Purchase += float(total)
        Supplier.save()
        Product_names=request.POST.getlist('Product')
        cRates=request.POST.getlist('rate')
        sRates=request.POST.getlist('sRate')
        quantities=request.POST.getlist('quantity')
        wc_ids = request.POST.getlist('wc_id')
        for i in range(len(Product_names)):
            product_name=Product_names[i]
            cRate=cRates[i]
            sRate=sRates[i]
            quantity=quantities[i]
            wc_id = wc_ids[i]

            product, created=Products.objects.get_or_create(ProductName=product_name)
            if created:
                product.wc_id = wc_id
            product.costPrice=cRate
            product.Rate=sRate
            product.Stock += float(quantity)
            purchaseDetail=PurchaseDetails.objects.create(
                Product=product,
                Quantity=quantity,
                Rate=cRate,
                sellRate=sRate,
                purchase=purchase
            )

            data = {
                'manage_stock': True,
                'stock_quantity': product.Stock
            }

            if product.wc_id is not None:
                wc.put(f"products/{product.wc_id}", data).json()

            product.save()
        return redirect('purchase')

    context={'suppliers':suppliers,'products':products}
    return render(request, 'base/purchase.html',context)

@login_required(login_url='login')
def get_supplier_details(request):
    supplier_name = request.GET.get('supplier_name')
    if supplier_name:
        suppliers = Suppliers.objects.filter(Sup_Name=supplier_name)
        supplier_numbers = list(suppliers.values_list('Cus_Number', flat=True))
        return JsonResponse({'numbers': supplier_numbers})
    return JsonResponse({'numbers': []})

@login_required(login_url='login')
def expenses(request):
    if request.method=='POST':
        purchaseFrom=request.POST.get('PurchaseFrom')
        total=request.POST.get('total')
        expense=Expense.objects.create(purchasedFrom=purchaseFrom,total=total)
        names=request.POST.getlist('names')
        amounts=request.POST.getlist('amounts')
        quantities=request.POST.getlist('quantities')
        rates=request.POST.getlist('rates')
        for i in range(len(names)):
            name=names[i]
            amount=amounts[i]
            quantity=quantities[i]
            rate=rates[i]
            ExpenseDetails.objects.create(
                name=name,
                quantity=quantity,
                rate=rate,
                Amount=amount,
                expense=expense
            )
        return redirect('expense')

    return render(request, 'base/expense.html')

@login_required(login_url='login')
def product(request):
    if request.method == 'POST':
        name=request.POST.get('product')
        stock=request.POST.get('stock')
        wc_id = request.POST.get('wc-id')
        cRate=request.POST.get('cRate')
        sRate=request.POST.get('sRate')
        stock = float(stock) if stock else 0
        product, created = Products.objects.get_or_create(
                ProductName=name,)
        if created:
            product.Rate = sRate
            product.costPrice = cRate
            product.Stock = stock
            product.wc_id = wc_id
            data = {
                'manage_stock': True,
                'stock_quantity': stock
            }

            if product.wc_id is not None:
                wc.put(f"products/{product.wc_id}", data).json()
            product.save()
        else:
            product.Rate = sRate
            product.costPrice = cRate
            product.Stock += stock

            data = {
                'manage_stock': True,
                'stock_quantity': product.Stock
            }

            if product.wc_id is not None:
                wc.put(f"products/{product.wc_id}", data).json()
            product.save()
        return redirect('product')
    return render(request,'base/Products.html')

@login_required(login_url='login')
def Customer(request):
    form = customerForm()
    if request.method == 'POST':
        form=customerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Customer')
    context={'form':form}
    return render(request,'base/Customer.html', context)

@login_required(login_url='login')
def report(request):
    return render(request, 'base/reports.html')

@login_required(login_url='login')
def salesReport(request):
    sales=Sales.objects.all()
    filters=saleFilter(request.GET, queryset=sales)
    sales=filters.qs
    
    per_page = request.GET.get('per_page', 10)
    if per_page == "all":  # Show all sales if "all" is selected
        paginated_sales = sales
    else:
        paginator = Paginator(sales, int(per_page))  # Paginate sales
        page_number = request.GET.get('page')
        paginated_sales = paginator.get_page(page_number)
    
    total_amount = sales.aggregate(total=Sum('TotalAmt'))['total']
    context={'sales':paginated_sales, 'filters':filters,'total_amount':total_amount,'per_page': per_page,}
    return render(request, 'base/SalesReport.html', context)

@login_required(login_url='login')
def viewSales(request, pk):
    sale=Sales.objects.get(id=pk)
    if sale.payment_method == 'credit':
        if request.method == 'POST':
            form = saleForm(request.POST, instance=sale)
            if form.is_valid():
                form.save()
                return redirect('sales-report')
        else:
            form = saleForm(instance=sale)
            return render(request, 'base/viewCreditsale.html', {'form': form, 'sale':sale})
    else:
        context={'sale':sale}
        return render(request, 'base/viewSales.html', context)

@login_required(login_url='login')
def deleteSales(request, pk):
    try:
        sale = Sales.objects.get(id=pk)
        customer = sale.Customer

        if request.method == 'POST':
            saledetail=sale.saledetails_set.all()
            for sell in saledetail:
                sell.Product.Stock += sell.Quantity
                sell.Product.save()
                
            if sale.TotalAmt:
                customer.Cus_Purchase -= sale.TotalAmt
                customer.save()  

            sale.delete() 
            return redirect('dashboard')
        
        context = {'obj': sale}
        return render(request, 'base/delete.html', context)

    except Sales.DoesNotExist:
        return redirect('dashboard')

@login_required(login_url='login')
def purchaseReport(request):
    purchase=Purchase.objects.all()
    filters=purchaseFilter(request.GET, queryset=purchase)
    purchase=filters.qs
    total_amount = purchase.aggregate(total=Sum('totalAmtPur'))['total']
    context={'purchases':purchase, 'filters':filters,'total_amount':total_amount}
    return render(request, 'base/PurchaseReport.html', context)

@login_required(login_url='login')
def viewPurchase(request, pk):
    purchase=Purchase.objects.get(id=pk)
    if purchase.payment_method == 'credit':
        if request.method == 'POST':
            form = purchaseForm(request.POST, instance=purchase)
            if form.is_valid():
                form.save()
                return redirect('purchase-report')
        else:
            form = purchaseForm(instance=purchase)
            return render(request, 'base/viewCreditPurchase.html', {'form': form, 'purchase':purchase})
    else:
        context={'purchase':purchase}
        return render(request, 'base/viewPurchase.html', context)

@login_required(login_url='login')
def deletePurchase(request, pk):
    try:
        purchase = Purchase.objects.get(id=pk)
        supplier = purchase.Supplier

        if request.method == 'POST':
            purdetail=purchase.purchasedetails_set.all()
            for pur in purdetail:
                pur.Product.Stock -= pur.Quantity
                pur.Product.save()

            if purchase.totalAmtPur:
                supplier.Sup_Purchase -= purchase.totalAmtPur
                supplier.save()  # Save the customer object

            purchase.delete()  # Delete the purchase object
            return redirect('dashboard')
        
        context = {'obj': purchase}
        return render(request, 'base/delete.html', context)

    except Purchase.DoesNotExist:
        return redirect('dashboard')

@login_required(login_url='login')
def expenseReport(request):
    expense=Expense.objects.all()
    filters=expenseFilter(request.GET, queryset=expense)
    expense=filters.qs
    total_amount = expense.aggregate(total=Sum('total'))['total']
    context={'expenses':expense, 'filters':filters,'total_amount':total_amount}
    return render(request, 'base/expenseReports.html', context)

@login_required(login_url='login')
def viewExpense(request, pk):
    expense=Expense.objects.get(id=pk)
    context={'expense':expense}
    return render(request, 'base/viewExpense.html', context)

@login_required(login_url='login')
def deleteExpense(request, pk):
    try:
        expense = Expense.objects.get(id=pk)

        if request.method == 'POST':

            expense.delete()  
            return redirect('dashboard')
        
        context = {'obj': expense}
        return render(request, 'base/delete.html', context)

    except Expense.DoesNotExist:
        return redirect('dashboard')

@login_required(login_url='login')
def stockReport(request):
    products=Products.objects.all()
    filters=productFilter(request.GET, queryset=products)
    products=filters.qs
    total_stock = products.aggregate(total_stock=Sum(F('Stock') * F('costPrice')))['total_stock']
    context={'products':products, 'filters':filters,'total_stock':total_stock}
    return render(request, 'base/stock.html', context)

@login_required(login_url='login')
def customerReport(request):
    customer=Customers.objects.all()
    filters=customerFilter(request.GET, queryset=customer)
    customer=filters.qs
    total_amount = 0
    for cus in customer:
        sales = cus.sales_set.all()
        total_sales = sales.aggregate(total=Sum('TotalAmt'))['total']
        total_amount += total_sales or 0

    context = {'customers': customer, 'filters': filters, 'total_amount': total_amount}
    return render(request, 'base/customerReport.html', context)

@login_required(login_url='login')
def viewCustomer(request, pk):
    customer=Customers.objects.get(id=pk)
    salesRecord=customer.sales_set.all()
    total_amount = salesRecord.aggregate(total=Sum('TotalAmt'))['total']
    context={'customer':customer,'salesRecord':salesRecord,'total_amount':total_amount}
    return render(request, 'base/viewCustomer.html', context)

@login_required(login_url='login')
def supplierReport(request):
    supplier=Suppliers.objects.all()
    filters=supplierFilter(request.GET, queryset=supplier)
    supplier=filters.qs
    total_amount = 0
    for sup in supplier:
        purchase = sup.purchase_set.all()
        total_purchase = purchase.aggregate(total=Sum('totalAmtPur'))['total']
        total_amount += total_purchase or 0
    context={'suppliers':supplier, 'filters':filters, 'total_amount':total_amount}
    return render(request, 'base/supplierReport.html', context)

@login_required(login_url='login')
def viewSupplier(request, pk):
    supplier=Suppliers.objects.get(id=pk)
    purchaseRecord=supplier.purchase_set.all()
    total_amount = purchaseRecord.aggregate(total=Sum('totalAmtPur'))['total']
    context={'supplier':supplier,'purchaseRecord':purchaseRecord,'total_amount':total_amount}
    return render(request, 'base/viewSupplier.html', context)

