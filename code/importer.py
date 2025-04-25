import os
import sys
import django
import csv
from django.utils.dateparse import parse_datetime
from django.contrib.auth.hashers import make_password

sys.path.append(os.path.abspath(os.path.join(__file__, *[os.pardir] * 3)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'my_inventory.settings'
django.setup()

from core.models import Admin, Category, Supplier, Item
from django.db import connection

filepath = './data_csv/'

def reset_table_sequence(model, sequence_name):
    model.objects.all().delete()
    with connection.cursor() as cursor:
        cursor.execute(f"ALTER SEQUENCE {sequence_name} RESTART WITH 1;")

def import_admins():
    reset_table_sequence(Admin, 'core_admin_id_seq')
    with open(filepath + 'admins.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        obj_create = []
        for row in reader:
            if not Admin.objects.filter(username=row['username']).exists():
                obj_create.append(Admin(
                    username=row['username'],
                    password=make_password(row['password']),
                    email=row['email'],
                    created_at=parse_datetime(row['created_at']),
                    updated_at=parse_datetime(row['updated_at'])
                ))
        Admin.objects.bulk_create(obj_create)
    print("Admin data imported successfully.")

def import_categories():
    reset_table_sequence(Category, 'core_category_id_seq')
    with open(filepath + 'categories.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        obj_create = []
        for row in reader:
            if Admin.objects.filter(id=row['created_by_id']).exists():
                obj_create.append(Category(
                    name=row['name'],
                    description=row['description'],
                    created_by_id=row['created_by_id'],
                    created_at=parse_datetime(row['created_at']),
                    updated_at=parse_datetime(row['updated_at'])
                ))
            else:
                print(f"Admin dengan ID {row['created_by_id']} tidak ditemukan, kategori {row['name']} dilewatkan.")
        Category.objects.bulk_create(obj_create)
    print("Category data imported successfully.")

def import_suppliers():
    reset_table_sequence(Supplier, 'core_supplier_id_seq')
    with open(filepath + 'suppliers.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        obj_create = []
        for row in reader:
            if Admin.objects.filter(id=row['created_by_id']).exists():
                obj_create.append(Supplier(
                    name=row['name'],
                    contact_info=row['contact_info'],
                    created_by_id=row['created_by_id'],
                    created_at=parse_datetime(row['created_at']),
                    updated_at=parse_datetime(row['updated_at'])
                ))
            else:
                print(f"Admin dengan ID {row['created_by_id']} tidak ditemukan, supplier {row['name']} dilewatkan.")
        Supplier.objects.bulk_create(obj_create)
    print("Supplier data imported successfully.")

def import_items():
    reset_table_sequence(Item, 'core_item_id_seq')
    with open(filepath + 'items.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        obj_create = []
        for row in reader:
            if Category.objects.filter(id=row['category_id']).exists() and Supplier.objects.filter(id=row['supplier_id']).exists():
                obj_create.append(Item(
                    name=row['name'],
                    description=row['description'],
                    price=row['price'],
                    quantity=row['quantity'],
                    category_id=row['category_id'],
                    supplier_id=row['supplier_id'],
                    created_by_id=row['created_by_id'],
                    created_at=parse_datetime(row['created_at']),
                    updated_at=parse_datetime(row['updated_at'])
                ))
            else:
                print(f"Data kategori atau supplier tidak ditemukan untuk item {row['name']}, item dilewatkan.")
        Item.objects.bulk_create(obj_create)
    print("Item data imported successfully.")

if __name__ == "__main__":
    import_admins()
    import_categories()
    import_suppliers()
    import_items()
    print("Data import process completed.")
