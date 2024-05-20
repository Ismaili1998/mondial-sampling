# Generated by Django 4.2.7 on 2024-05-12 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commercialOffer', '0010_alter_commercialoffer_rank_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='commercialoffer',
            options={'ordering': ['-rank']},
        ),
        migrations.AlterModelOptions(
            name='confirmed_commercialoffer',
            options={'ordering': ['-rank']},
        ),
        migrations.AlterField(
            model_name='commercialoffer',
            name='rank',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='confirmed_commercialoffer',
            name='rank',
            field=models.IntegerField(default=0),
        ),
    ]