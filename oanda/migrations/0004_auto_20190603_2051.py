# Generated by Django 2.2 on 2019-06-03 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oanda', '0003_auto_20190602_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='external_id',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
