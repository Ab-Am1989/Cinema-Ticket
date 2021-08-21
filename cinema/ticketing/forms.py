from django import forms
from ticketing.models import Cinema

class ShowTimeSearchForm(forms.Form):
    movie_name = forms.CharField(max_length=100,label='نام فیلم',required=False)
    sale_open_only = forms.BooleanField(label='فقط سانس‌های قابل خرید',required=False)
    movie_min_length = forms.IntegerField(label='حدأقل زمان فیلم',min_value=0,max_value=200,required=False)
    movie_max_length = forms.IntegerField(label='حدأکثر زمان فیلم',min_value=0,max_value=200,required=False)

    PRICE_ANY = '0'
    PRICE_UNDER_10 = '1'
    PRICE_10to15 = '2'
    PRICE_15to20 = '3'
    PRICE_ABOVE_20 = '4'

    PRICE_LEVEL_CHOICES = [
        (PRICE_ANY,'هر قیمتی'),
        (PRICE_UNDER_10,' کمتر از  ۱۰ هزار تومان'),
        (PRICE_10to15,' از ۱۰ هزار تا ۱۵ هزار تومان'),
        (PRICE_15to20,' از ۱۵ تا ۲۰ هزار تومان'),
        (PRICE_ABOVE_20,' بالاتر از ۲۰ هزار تومان')
    ]

    price_level = forms.ChoiceField(label='محدوده قیمت',choices=PRICE_LEVEL_CHOICES,required=False)
    
    cinema = forms.ModelChoiceField(label='انتخاب سینما',queryset=Cinema.objects.all(),required=False)

    def get_price_boundries(self):
        price_level = self.cleaned_data['price_level']
        if price_level == ShowTimeSearchForm.PRICE_UNDER_10:
            return None,10000
        elif price_level == ShowTimeSearchForm.PRICE_10to15:
            return 10000,15000
        elif price_level == ShowTimeSearchForm.PRICE_15to20:
            return 15000,20000
        elif price_level == ShowTimeSearchForm.PRICE_ABOVE_20:
            return 20000,None
        else:
            return None,None