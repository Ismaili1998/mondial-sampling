# Generated by Django 4.2.7 on 2023-11-19 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_alter_country_country_name_en_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='abbreviation',
            field=models.CharField(max_length=4),
        ),
    ]
