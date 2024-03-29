# Generated by Django 4.1 on 2023-03-28 06:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer_db', '0004_rename_require_ddate_orders_required_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Occupation',
            fields=[
                ('title', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('avg_salary', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('person_id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('occupation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='person', to='customer_db.occupation')),
            ],
        ),
    ]
