# Generated by Django 4.1 on 2023-03-26 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_db', '0002_rename_postalcode_customers_postal_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('product_code', models.CharField(db_column='productCode', max_length=15, primary_key=True, serialize=False)),
                ('product_name', models.CharField(db_column='productName', max_length=70)),
                ('product_scale', models.CharField(db_column='productScale', max_length=10)),
                ('product_vendor', models.CharField(db_column='productVendor', max_length=50)),
                ('product_description', models.TextField(db_column='productDescription')),
                ('quantity_in_stock', models.SmallIntegerField(db_column='quantityInStock')),
                ('buy_price', models.DecimalField(db_column='buyPrice', decimal_places=2, max_digits=10)),
                ('msrp', models.DecimalField(db_column='msrp', decimal_places=2, max_digits=10)),
            ],
            options={
                'db_table': 'products',
            },
        ),
    ]
