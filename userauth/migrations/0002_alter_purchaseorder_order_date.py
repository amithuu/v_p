# Generated by Django 5.0.4 on 2024-05-07 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='order_date',
            field=models.DateTimeField(),
        ),
    ]
