# Generated by Django 4.1 on 2023-03-27 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer_db', '0003_products'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orders',
            old_name='require_ddate',
            new_name='required_date',
        ),
    ]
