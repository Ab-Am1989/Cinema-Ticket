import re
from django import forms
from accounts.models import Payment, Profile
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserChangeForm
class PaymentForm(forms.ModelForm):
    
    class Meta:
        model = Payment
        fields = ['amount','transaction_code']
    def clean(self):
        super().clean()
        amount = self.cleaned_data.get('amount')
        code = self.cleaned_data.get('transaction_code')
        if amount is not None and code is not None:
            if int(code.split('-')[1]) != amount:
                raise ValidationError('مبلغ و رسید تراکش بایکدیگر هم‌خوانی ندارند')

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount%1000 != 0:
            raise ValidationError('مبلغ تراکنش باید ضریبی از هزار تومان باشد')
        return amount

    def clean_transaction_code(self):
        regex = r'^bank-\d{4,6}-.+-\#$'
        code = self.cleaned_data.get('transaction_code')
        is_match = re.match(regex,code)
        if is_match is None:
            raise ValidationError('فرمت رسید تراکنش صحیح نیست')
        else:
            return code
class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ('mobile','gender','address','profie_image')

class UserForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        fields =['first_name','last_name','email']