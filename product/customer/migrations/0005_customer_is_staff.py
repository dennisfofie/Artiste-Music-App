# Generated by Django 4.1.7 on 2023-03-21 20:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("customer", "0004_remove_customer_full_name_customer_username"),
    ]

    operations = [
        migrations.AddField(
            model_name="customer",
            name="is_staff",
            field=models.BooleanField(default=False),
        ),
    ]
