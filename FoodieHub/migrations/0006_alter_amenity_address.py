# Generated by Django 4.2.5 on 2024-01-01 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FoodieHub', '0005_alter_amenity_location_alter_profile_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amenity',
            name='address',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
