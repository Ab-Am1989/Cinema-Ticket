# Generated by Django 2.2.1 on 2021-04-01 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('director', models.CharField(max_length=50)),
                ('year', models.IntegerField()),
                ('length', models.IntegerField()),
                ('description', models.TextField()),
            ],
        ),
    ]
