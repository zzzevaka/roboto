# Generated by Django 2.2 on 2019-07-04 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oanda', '0007_auto_20190704_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='created_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='trade',
            name='pl',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='created_at',
            field=models.DateTimeField(null=True),
        ),
    ]
