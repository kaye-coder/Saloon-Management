# Generated by Django 5.1.4 on 2024-12-07 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_remove_customer_branch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
