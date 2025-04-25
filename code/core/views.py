from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Avg, F, Count
from django.contrib import messages
from .models import Item, Category, Supplier, Admin
from .forms import ItemForm, CategoryForm, SupplierForm

def dashboard(request):
    total_items = Item.objects.count()
    total_stock_value = Item.objects.aggregate(
        total=Sum(F('price') * F('quantity'))
    )['total'] or 0
    total_categories = Category.objects.count()
    total_suppliers = Supplier.objects.count()
    
    context = {
        'total_items': total_items,
        'total_stock_value': total_stock_value,
        'total_categories': total_categories,
        'total_suppliers': total_suppliers,
    }
    return render(request, '../templates/dashboard.html', context)

def item_list(request):
    items = Item.objects.all()
    stats = Item.objects.aggregate(
        total_stock=Sum('quantity'),
        total_value=Sum(F('price') * F('quantity')),
        avg_price=Avg('price')
    )
    low_stock_items = Item.objects.filter(quantity__lt=10)
    
    for item in items:
        item.total_value = item.price * item.quantity
        
    context = {
        'items': items,
        'stats': stats,
        'low_stock_items': low_stock_items,
    }
    return render(request, '../templates/item_page.html', context)

def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            try:
                admin = Admin.objects.get(username='admin1')
                item.created_by = admin
            except Admin.DoesNotExist:
                messages.error(request, 'Hanya Admin yang dapat melalukan fitur ini.')
                return redirect('item_list')
            item.save()
            messages.success(request, 'Item successfully added.')
            return redirect('item_list')
    else:
        form = ItemForm()
    
    return render(request, '../templates/addItem.html', {'form': form})

def category_list(request):
    categories = Category.objects.annotate(
        item_count=Count('item'),
        total_value=Sum(F('item__price') * F('item__quantity')),
        avg_price=Avg('item__price')
    )
    return render(request, '../templates/category_page.html', {'categories': categories})

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            try:
                admin = Admin.objects.get(username='admin1')
                category.created_by = admin
            except Admin.DoesNotExist:
                messages.error(request, 'Hanya Admin yang dapat melalukan fitur ini.')
                return redirect('category_list')
            category.save()
            messages.success(request, 'Category successfully added.')
            return redirect('category_list')
    else:
        form = CategoryForm()
    
    return render(request, '../templates/addCategory.html', {'form': form})

def supplier_list(request):
    suppliers = Supplier.objects.annotate(
        item_count=Count('item'),
        total_value=Sum(F('item__price') * F('item__quantity'))
    )
    return render(request, '../templates/suppliers_page.html', {'suppliers': suppliers})

def supplier_create(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save(commit=False)
            try:
                admin = Admin.objects.get(username='admin1')
                supplier.created_by = admin
            except Admin.DoesNotExist:
                messages.error(request, 'Hanya Admin yang dapat melalukan fitur ini.')
                return redirect('supplier_list')
            supplier.save()
            messages.success(request, 'Supplier successfully added.')
            return redirect('supplier_list')
    else:
        form = SupplierForm()
    
    return render(request, '../templates/addSuppliers.html', {'form': form})

def category_items(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    items = Item.objects.filter(category=category)

    item_count = items.count()
    total_value = items.aggregate(total=Sum(F('price') * F('quantity')))['total'] or 0
    avg_price = items.aggregate(avg=Avg('price'))['avg'] or 0
    total_stock = items.aggregate(total=Sum('quantity'))['total'] or 0

    category.item_count = item_count
    category.total_value = total_value
    category.avg_price = avg_price

    context = {
        'category': category,
        'items': items,
        'total_stock': total_stock,
    }

    return render(request, '../templates/categoryItem_page.html', context)