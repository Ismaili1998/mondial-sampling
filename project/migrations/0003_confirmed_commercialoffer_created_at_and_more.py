# Generated by Django 4.2.7 on 2023-11-04 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_remove_article_selling_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='confirmed_commercialoffer',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='confirmed_commercialoffer',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
