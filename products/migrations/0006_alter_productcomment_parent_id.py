# Generated by Django 4.1.13 on 2024-05-25 11:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_category_thumbnail_url_alter_category_icon_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcomment',
            name='parent_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.productcomment'),
        ),
    ]