# Generated by Django 2.2.1 on 2021-06-16 07:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=11, verbose_name='تلفن همراه')),
                ('gender', models.IntegerField(blank=True, choices=[(1, 'مرد'), (2, 'زن'), (3, 'سایر')], null=True, verbose_name='جنسیت')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='تاریخ تولد')),
                ('address', models.TextField(blank=True, null=True, verbose_name='آدرس')),
                ('profie_image', models.ImageField(blank=True, null=True, upload_to='users/profile_images/', verbose_name='تصویر')),
                ('balance', models.IntegerField(default=0, verbose_name='اعتبار')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='حساب کاربری')),
            ],
            options={
                'verbose_name': 'نمایه کاربری',
                'verbose_name_plural': 'نمایه کاربری',
            },
        ),
    ]
