# Generated by Django 2.2.1 on 2021-04-03 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cinema',
            fields=[
                ('cinema_code', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('city', models.CharField(default='تهران', max_length=30)),
                ('capcity', models.IntegerField()),
                ('phone', models.CharField(max_length=20, null=True)),
                ('address', models.TextField()),
            ],
        ),
    ]