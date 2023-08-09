from django.db import models
from .custom_models import *
from .hospital_models import *


class Customers(models.Model):
    customer_number = models.IntegerField(db_column="customerNumber", primary_key=True)
    customer_name = models.CharField(db_column="customerName", max_length=50)
    contact_last_name = models.CharField(db_column="contactLastName", max_length=50)
    contact_first_name = models.CharField(db_column="contactFirstName", max_length=50)
    phone = models.CharField(max_length=50)
    address_line1 = models.CharField(db_column="addressLine1", max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50, blank=True, null=True)
    postal_code = models.CharField(
        db_column="postalCode", max_length=15, blank=True, null=True
    )
    country = models.CharField(max_length=50)

    class Meta:
        db_table = "customers"


class Orders(models.Model):
    order_number = models.IntegerField(db_column="orderNumber", primary_key=True)
    order_date = models.DateField(db_column="orderDate")
    required_date = models.DateField(db_column="requiredDate")
    shipped_date = models.DateField(db_column="shippedDate", blank=True, null=True)
    status = models.CharField(max_length=15)
    comments = models.TextField(blank=True, null=True)
    customer_number = models.ForeignKey(
        Customers, models.DO_NOTHING, db_column="customerNumber"
    )

    class Meta:
        db_table = "orders"


class Products(models.Model):
    product_code = models.CharField(
        db_column="productCode", primary_key=True, max_length=15
    )
    product_name = models.CharField(db_column="productName", max_length=70)
    product_scale = models.CharField(db_column="productScale", max_length=10)
    product_vendor = models.CharField(db_column="productVendor", max_length=50)
    product_description = models.TextField(db_column="productDescription")
    quantity_in_stock = models.SmallIntegerField(db_column="quantityInStock")
    buy_price = models.DecimalField(
        db_column="buyPrice", max_digits=10, decimal_places=2
    )
    msrp = models.DecimalField(db_column="msrp", max_digits=10, decimal_places=2)

    class Meta:
        db_table = "products"
