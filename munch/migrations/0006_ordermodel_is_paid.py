# Generated by Django 4.0.6 on 2022-07-22 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('munch', '0005_rename_zip_code_ordermodel_zip'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordermodel',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
    ]
