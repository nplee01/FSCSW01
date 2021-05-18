# From Django
from django.utils.translation import ugettext_lazy as _ # To mark strings for translations
from django.db import models

class historySet(models.Model):
    number = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    stock_ticker = models.CharField(max_length=4)
    test_parameter = models.CharField(max_length=64)
    percent_winning_trade = models.FloatField()
    average_win = models.FloatField()
    remark = models.CharField(max_length=512)
