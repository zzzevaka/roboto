# Generated by Django 2.2 on 2019-06-16 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0003_auto_20190616_1007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='learningmodel',
            name='file',
            field=models.FileField(null=True, upload_to='learning_models/'),
        ),
    ]