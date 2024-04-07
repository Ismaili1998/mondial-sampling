# Generated by Django 4.2.7 on 2024-03-17 22:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project', '0005_alter_project_client'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdvancePayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('comment', models.TextField(blank=True, max_length=400, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('representative', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.representative')),
            ],
            options={
                'db_table': 'advance_payment',
                'ordering': ['-created_at'],
            },
        ),
    ]
