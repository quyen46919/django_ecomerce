# Generated by Django 4.1.13 on 2024-05-24 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_category_icon_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='thumbnail_url',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='icon_url',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
    ]
