# Generated by Django 5.0.1 on 2024-01-11 08:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='address_receiver',
            new_name='receiver_address',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='name_receiver',
            new_name='receiver_name',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='phone_receiver',
            new_name='receiver_phone',
        ),
    ]
