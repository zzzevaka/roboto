# Generated by Django 2.2 on 2019-06-03 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roboto', '0002_auto_20190603_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instrument',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
