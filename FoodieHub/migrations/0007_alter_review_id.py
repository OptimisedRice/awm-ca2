# Generated by Django 4.2.5 on 2024-01-01 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FoodieHub', '0006_alter_amenity_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
