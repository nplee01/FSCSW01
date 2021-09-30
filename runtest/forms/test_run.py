from datetime import date
# Django Modules
from django.utils.translation import ugettext_lazy as _ # To mark strings for translation
from django.forms import ChoiceField, IntegerField, ValidationError

# Our modules
from runtest.models import TestRun, ValueSet, ValueSetMember
from .version_model_form import VersionModelForm

class TestRunForm(VersionModelForm):
    """
    Test Run form to allow user to select input parameters for a Backtest Run.
    """
    # Override from Text to Select widget 
    stock_ticker = ChoiceField(label=_("Stock Name"), required=True,
            help_text=_("Stock to be selected for this backtest run"))
    strategy_code = ChoiceField(label=_("Strategy"), required=True,
            help_text=_("Strategy to use when triggering trades using Indicators"))
    indicator_1_code = ChoiceField(label=_("Indicator 1"), required=True, 
            help_text=_("Indicator 1 used for this backtest run"))
    indicator_2_code = ChoiceField(label=_("Indicator 2"), required=False,
            help_text=_("Indicator 2 used for this backtest run"))
    # Indicator 3 Not used
    # Disabled fields
    portfolio_start = IntegerField(label=_("Initial Capital"), disabled=True, 
            help_text=_("Backtest will start with this initial capital amount"))
    trade_size = IntegerField(label=_("Trade Size"), disabled=True, help_text=_("Units per Trade"))

    class Meta:
        model = TestRun
        # All other fields are updated by program, last_version is needed for optimistic locking
        fields = ['stock_ticker', 'start_date', 'end_date', 'portfolio_start', 'strategy_code', 
                'indicator_1_code', 'ind_1_param_1', 'ind_1_param_2', 'ind_1_param_3', 
                'ind_1_param_4', 'ind_1_param_5',
                'indicator_2_code', 'ind_2_param_1', 'ind_2_param_2', 'ind_2_param_3', 
                'ind_2_param_4', 'ind_2_param_5', 'trade_size', 'last_version' ]

    def __init__(self, *args, **kwargs):
        # Call parent's init method
        super().__init__(*args, **kwargs)
        # Populate choices from Value Set for Stock tickers
        try:
            vs = ValueSet.objects.get(value_set_code='STOCKS')
            choices = vs.get_choices()
        except ValueSet.DoesNotExist:
            choices = []
        # Attach choices to widget
        self.fields["stock_ticker"].choices = choices
        # Populate choices from Value Set for Strategy
        try:
            vs = ValueSet.objects.get(value_set_code='STRATEGIES')
            choices = vs.get_choices()
        except ValueSet.DoesNotExist:
            choices = []
        # Attach choices to widget
        self.fields["strategy_code"].choices = choices
        # Populate choices from Value Set for Indicators
        try:
            vs = ValueSet.objects.get(value_set_code='INDICATORS')
            choices = vs.get_choices()
        except ValueSet.DoesNotExist:
            choices = []
        # Attach choices to widget
        self.fields["indicator_1_code"].choices = choices
        self.fields["indicator_2_code"].choices = choices

    def clean(self):
        # Form validation
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if start_date > end_date:
            raise ValidationError(f"Start date {start_date} must be earlier than End date {end_date}")
        ticker = cleaned_data.get("stock_ticker")
        # Ticker may not be present if failed validation
        if ticker:
            # Check that data available for date range
            vs = ValueSet.objects.get(value_set_code='STOCKS')
            stock = ValueSetMember.objects.get(value_set=vs, value_code=ticker)
            # We store date as ordinal in Parameter
            dl_start = date.fromordinal(stock.param_1.default_value)
            dl_end = date.fromordinal(stock.param_2.default_value)
            # Validate that the start/end requested within range
            if start_date < dl_start or end_date > dl_end:
                raise ValidationError(f'Start or End date beyond our available range of {dl_start} to {dl_end}')
        # Validation ok
        return cleaned_data
