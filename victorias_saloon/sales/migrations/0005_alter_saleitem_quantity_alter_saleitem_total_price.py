# Generated by Django 5.1.4 on 2025-01-17 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0004_alter_sale_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saleitem',
            name='quantity',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='saleitem',
            name='total_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
