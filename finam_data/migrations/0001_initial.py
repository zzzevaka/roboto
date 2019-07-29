# Generated by Django 2.2 on 2019-07-28 09:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Instrument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('market', models.SmallIntegerField(choices=[(0, 'Currencies')])),
            ],
            options={
                'verbose_name': 'Frinam instrument',
                'verbose_name_plural': 'Finame models',
            },
        ),
        migrations.CreateModel(
            name='Candle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('granularity', models.IntegerField(choices=[(1, '1 hour')])),
                ('time', models.DateTimeField(db_index=True)),
                ('instrument', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finam_data.Instrument')),
            ],
            options={
                'verbose_name': 'Finam candle',
                'verbose_name_plural': 'Finam candles',
            },
        ),
    ]
