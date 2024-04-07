# Generated by Django 4.2.7 on 2024-03-20 15:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0006_alter_client_country_alter_client_language_and_more'),
        ('commercialOffer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commercialoffer',
            name='currency',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='project.currency'),
        ),
        migrations.AlterField(
            model_name='commercialoffer',
            name='delivery_time_unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='project.timeunit'),
        ),
        migrations.AlterField(
            model_name='commercialoffer',
            name='destination',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='project.destination'),
        ),
        migrations.AlterField(
            model_name='commercialoffer',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='project.payment'),
        ),
        migrations.AlterField(
            model_name='commercialoffer',
            name='shipping',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='project.shipping'),
        ),
        migrations.AlterField(
            model_name='commercialoffer',
            name='transport',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='project.transport'),
        ),
        migrations.AlterField(
            model_name='confirmed_commercialoffer',
            name='commercialOffer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='commercialOffer.commercialoffer'),
        ),
    ]
