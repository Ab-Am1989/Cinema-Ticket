from django.db import models
from accounts.models import Profile
class Movie(models.Model):
    class Meta:
        verbose_name = 'فیلم'
        verbose_name_plural = 'فیلم'
    name = models.CharField('نام فیلم', max_length=100)
    director = models.CharField('کارگردان', max_length=50)
    year = models.IntegerField('سال تولید')
    length = models.IntegerField('زمان')
    description = models.TextField('خلاصه داستان')
    poster = models.ImageField('پوستر', upload_to='movie_posters/')

    def __str__(self):
        return self.name

        
class Cinema(models.Model):
    class Meta:
        verbose_name = 'سینما'
        verbose_name_plural = 'سینما'
    cinema_code = models.IntegerField(primary_key=True)
    name = models.CharField('نام سینما',max_length = 50)
    city = models.CharField('شهر',max_length = 30, default='تهران')
    capacity = models.IntegerField('ظرفیت')
    phone = models.CharField('شماره تماس',max_length = 20, blank=True)
    address = models.TextField('آدرس',blank=True)
    image = models.ImageField('تصویر',upload_to='cinema_images/',null=True,blank=True)
    
    
    def __str__(self):
        return self.name

class ShowTime(models.Model):
    class Meta:
        verbose_name = 'سانس'
        verbose_name_plural = 'سانس'

    movie = models.ForeignKey('Movie', on_delete=models.PROTECT, verbose_name='فیلم')
    cinema = models.ForeignKey('Cinema', on_delete=models.PROTECT, verbose_name='سینما')
    
    start_time = models.DateTimeField('زمان شروع')
    price = models.IntegerField('قیمت')
    saleable_seats = models.IntegerField('تعداد قابل فروش')
    free_seats = models.IntegerField('تعداد باقی‌مانده')
    
    SALE_NOT_STARTED = 1
    SALE_OPEN = 2
    TICKET_SOLD = 3
    SALE_CLOSED = 4
    MOVIE_PLAYED = 5
    SHOW_CANCELED = 6

    status_choices = (
        (SALE_NOT_STARTED,'فروش شروع نشده '),
        (SALE_OPEN,'درحال فروش بلیط'),
        (TICKET_SOLD,'بلیط تمام شد'),
        (SALE_CLOSED,'فروش بلیط بسته شده '),
        (MOVIE_PLAYED,'فیلم پخش شد'),
        (SHOW_CANCELED, 'سانس لغو شد'),
    )

    status = models.IntegerField('وضعیت',choices=status_choices)

    def __str__(self):
        return '{}-{}-{}'.format(self.movie,self.cinema,self.start_time)
    

    def get_price_display(self):
        return '{}'.format(self.price)
    
    def reserve_seats(self,seat_count):
        assert isinstance(seat_count,int) and seat_count>0,'Number of seats should be integer'
        assert self.status == ShowTime.SALE_OPEN , 'Sale isn\'t open '
        assert self.free_seats >= seat_count , 'Not enough free seats'
        self.free_seats -= seat_count
        if self.free_seats == 0 :
            self.status = ShowTime.TICKET_SOLD
        self.save()

class Ticket(models.Model):
    class Meta:
        verbose_name = 'بلیت'
        verbose_name_plural = 'بلیت'
    
    showtime = models.ForeignKey('ShowTime',on_delete=models.PROTECT,verbose_name='سانس')
    customer = models.ForeignKey('accounts.Profile',on_delete=models.PROTECT,verbose_name='خریدار')
    seat_count = models.IntegerField('تعداد صندلی')
    order_time = models.DateTimeField('زمان خرید',auto_now_add=True)

    def __str__(self):
        return "{}بلیت به نام {} برای فیلم {}".format(self.seat_count,self.customer,self.showtime.movie) 