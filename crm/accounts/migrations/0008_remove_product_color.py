# Generated by Django 3.2 on 2021-06-28 07:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_product_color'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='color',
        ),
    ]
