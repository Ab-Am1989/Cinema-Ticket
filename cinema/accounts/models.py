from django.db import models
from django.contrib.auth.models import User
from django.db.models.query import FlatValuesListIterable
# Create your models here.

class Profile(models.Model):
    class Meta:
        verbose_name = 'نمایه کاربری'
        verbose_name_plural = 'نمایه کاربری'

    user = models.OneToOneField(User,on_delete=models.CASCADE,verbose_name='حساب کاربری')
    mobile = models.CharField('تلفن همراه',max_length=11)
    MALE = 1
    FEMALE = 2
    OTHER = 3
    GENDER_CHOICES = ((MALE,'مرد'),(FEMALE,'زن'),(OTHER, 'سایر'))
    gender = models.IntegerField('جنسیت',choices=GENDER_CHOICES,null=True,blank=True)
    birth_date = models.DateField('تاریخ تولد',null=True,blank=True)
    address = models.TextField('آدرس',null=True,blank=True)
    profie_image = models.ImageField('تصویر',upload_to='users/profile_images/',null=True,blank=True)
    balance = models.IntegerField('اعتبار',default=0)

    def __str__(self):
        return self.user.get_full_name()

    def get_balance_display(self):
        return '{} تومان'.format(self.balance)
    
    def deposit(self,amount):
        self.balance += amount
        self.save()
    
    def spend(self,amount):
        if self.balance < amount:
            return False
        
        self.balance -= amount
        self.save()
        return True

class Payment(models.Model):
    class Meta:
        verbose_name = 'پرداخت'
        verbose_name_plural = 'پرداخت'
    
    profile = models.ForeignKey('Profile',on_delete=models.CASCADE,verbose_name='کاربر')
    amount = models.PositiveIntegerField('مبلغ')
    transaction_time = models.DateTimeField('زمان تراکنش', auto_now_add=True)
    transaction_code = models.CharField('رسید تراکنش', max_length=30)

    def __str__(self):
        return 'مبلغ {}تومان به حساب کاربری {}اضافه شد'.format(self.amount,self.profile)
