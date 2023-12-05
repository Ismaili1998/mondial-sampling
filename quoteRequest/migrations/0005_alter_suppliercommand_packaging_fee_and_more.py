# Generated by Django 4.2.7 on 2023-12-03 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quoteRequest', '0004_alter_suppliercommand_packaging_fee_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suppliercommand',
            name='packaging_fee',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='suppliercommand',
            name='transport_fee',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
    ]
