# Generated by Django 4.2.10 on 2024-02-16 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_customuser_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_worker',
            field=models.BooleanField(default=False),
        ),
    ]
