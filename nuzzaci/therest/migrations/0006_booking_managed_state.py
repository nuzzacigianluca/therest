# Generated by Django 5.0.2 on 2024-05-24 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('therest', '0005_alter_booking_data_alter_booking_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking_managed',
            name='state',
            field=models.BooleanField(null=True),
        ),
    ]