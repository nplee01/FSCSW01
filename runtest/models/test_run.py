# From Django
from django.utils.translation import ugettext_lazy as _ # To mark strings for translations
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone 

# Our modules
from .record_owner import RecordOwner
from runtest.constants import DATETIME_FORMAT, RANGE_SEPARATOR

# User model may be overridden by us
User = get_user_model()

class TestRun(RecordOwner):
    """
    Every Backtest run executed will have a row stored here.

    It will store the input parameters selected by the user
    and save the results summary. The trades triggered by the
    backtest run will be stored in its child model TestRunResult.

    Only logged in users can save a TestRun row. Guest users will
    have the data saved temporarily in threadlocals when
    they are lost when they exit or saved when they successfully
    login.
    """

    # User who ran this test, optional when user is a guest but we should never save w/o user
    run_by = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name=_("User"))
    # Run status, QUE=Queued, EXE=Executing, COM=Completed
    run_status = models.CharField(verbose_name=_("Run Status"), default='QUE', max_length=3,
            help_text=_("Status of this test run"))
    run_on = models.DateTimeField(verbose_name=_("Run On"))
    # May be delayed if we queue the test runs later on
    exec_start_on = models.DateTimeField(verbose_name=_("Execution Started On"), null=True)
    exec_end_on = models.DateTimeField(verbose_name=_("Execution Ended On"), null=True)
    # Keep track of trades made for this test run
    last_trade_no = models.PositiveIntegerField(verbose_name=_("Last Trade No"), default=0,
            null=True)
    # Allow user to make notes about the run
    user_remarks = models.CharField(verbose_name=_("Remarks"), max_length=400, null=True, blank=True,
            help_text=_("Your notes about this run for future reference"))
    # Input parameters ....
    # Initially allow 1 stock, later can be comma delimited each max=30. Empty choices is to
    # make it a ChoiceField in its form.
    stock_ticker = models.CharField(verbose_name=_("Stock Name"), max_length=200, 
            choices=[], help_text=_("Stock to be selected for this backtest run"))
    # Start/End date range for backtest
    start_date = models.DateField(verbose_name=_("Start Date"), help_text=_("Backtest to start from this date"))
    end_date = models.DateField(verbose_name=_("End Date"), help_text=_("Backtest to end on this date"))
    # Portfolio starting amount
    portfolio_start = models.IntegerField(verbose_name=_("Starting Capital"),
            help_text=_("Backtest will start with this starting capital amount"), default=100000)
    # Strategy selected (from ValueSet(STRATEGIES))
    strategy_code = models.CharField(verbose_name=_("Strategy"), max_length=30,
            choices=[], help_text=_("Strategy to use when triggering trades using Indicators"))
    stop_loss = models.FloatField(verbose_name=_("Stop Loss"), null=True,
            help_text=_("Triggers sell when % loss hit this level based on cost price"))
    # Not used for now
    trail_stop_loss = models.FloatField(verbose_name=_("Trailing Stop Loss"), null=True, blank=True,
            help_text=_("Triggers sell when losses hit this level based on current value"))
    # Up to 3 indicators used in this run. Selected from ValueSet(INDICATORS)
    # Each indicator may have up to 3 parameters of int value
    indicator_1_code = models.CharField(verbose_name=_("Indicator 1"), max_length=30, null=True, blank=True,
        choices=[], help_text=_("Indicator 1 used for this backtest run"))
    ind_1_param_1 = models.IntegerField(verbose_name=_("Param 1"), null=True, blank=True)
    ind_1_param_2 = models.IntegerField(verbose_name=_("Param 2"), null=True, blank=True)
    ind_1_param_3 = models.IntegerField(verbose_name=_("Param 3"), null=True, blank=True)
    indicator_2_code = models.CharField(verbose_name=_("Indicator 2"), max_length=30, null=True, blank=True,
        choices=[], help_text=_("Indicator 2 used for this backtest run"))
    ind_2_param_1 = models.IntegerField(verbose_name=_("Param 1"), null=True, blank=True)
    ind_2_param_2 = models.IntegerField(verbose_name=_("Param 2"), null=True, blank=True)
    ind_2_param_3 = models.IntegerField(verbose_name=_("Param 3"), null=True, blank=True)
    indicator_3_code = models.CharField(verbose_name=_("Indicator 3"), max_length=30, null=True, blank=True,
        choices=[], help_text=_("Indicator 3 used for this backtest run"))
    ind_3_param_1 = models.IntegerField(verbose_name=_("Param 1"), null=True, blank=True)
    ind_3_param_2 = models.IntegerField(verbose_name=_("Param 2"), null=True, blank=True)
    ind_3_param_3 = models.IntegerField(verbose_name=_("Param 3"), null=True, blank=True)
    # Trade Sizing Method
    sizing_method = models.CharField(verbose_name=_("Sizing Method"), max_length=30, null=True, blank=True,
        help_text=_("Trade Sizing method decides how much to trade"))
    trade_size = models.IntegerField(verbose_name=_(""), null=True, default=1000,
        help_text=_(""))
    # End Input Parameters
    # Results Summary. To be updated after run
    portfolio_end = models.IntegerField(verbose_name=_("Final Capital"), null=True,
            help_text=_("Final Capital Amount when Backtest Ends"))
    win_trades = models.PositiveIntegerField(verbose_name=_("Winning Trades"), null=True,
        help_text=_("Number of winning trades made"))
    lose_trades = models.PositiveIntegerField(verbose_name=_("Losing Trades"), null=True,
        help_text=_("Number of losing trades made"))
    avg_win_amount = models.IntegerField(verbose_name=_("Average Win"), null=True,
            help_text=_("Average winning amount per trade"))
    avg_loss_amount = models.IntegerField(verbose_name=_("Average Loss"),null=True,
            help_text=_("Average losing amount per trade"))
    sharpe_ratio = models.FloatField(verbose_name=_("Sharpe Ratio"), null=True)
    sqn_no = models.FloatField(verbose_name=_("SQN No"), null=True)
    
    class Meta:
        db_table = 'test_run'
        unique_together = ['run_by', 'run_on']

    def __str__(self):
        return str(self.run_by) + RANGE_SEPARATOR + timezone.localtime(self.run_on).strftime(DATETIME_FORMAT)
    
    def save(self, force_insert=False, force_update=False):
        if self.run_on is None:
            self.run_on = timezone.now()
        # Perform the actual save
        super().save(force_insert, force_update)

class TestRunResult(RecordOwner):
    """
    Child model of TestRun to store all trades triggered by the Indicators.

    This model should not be editable (ie updated in a form) but created based
    on backtest results.
    """
    # Parent model
    test_run = models.ForeignKey(TestRun, on_delete=models.PROTECT, verbose_name=_("Test Run"))
    trade_no = models.PositiveIntegerField(verbose_name=_("Trade No"))
    # Trade details
    trade_date = models.DateField(verbose_name=_("Trade Date"))
    stock_ticker = models.CharField(verbose_name=_("Stock Ticker"), max_length=30)
    buy_flag = models.CharField(verbose_name=_("Buy Flag (B/S)"), max_length=1)
    trade_quantity = models.PositiveIntegerField(_("Trade Quantity"))
    trade_price = models.DecimalField(_("Traded Price"), max_digits=15, decimal_places=5)
    trade_amount = models.DecimalField(_("Trade Amount"), max_digits=15, decimal_places=2)
    # Fields below to be updated for Buy trades only (by subsequent Sell trades on FIFO basis)
    avg_sell_price = models.DecimalField(_("Average Sell Price"), max_digits=15, decimal_places=5)
    sell_amount = models.DecimalField(_("Sell Amount"), max_digits=15, decimal_places=2)
    # Profit is sell - buy amount (when fully sold), -ve means loss
    # Win when profit +ve
    win_flag = models.BooleanField(_("Winning Trade?"), null=True)

    class Meta:
        db_table = 'test_run_result'
        unique_together = ['test_run', 'trade_no']

    def __str__(self):
        # Should display together with parent 
        return str(self.trade_no)
