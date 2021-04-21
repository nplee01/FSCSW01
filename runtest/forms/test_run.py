# Django Modules
from django.utils.translation import ugettext_lazy as _ # To mark strings for translation

# Our modules
from runtest.models import TestRun, ValueSet
from .version_model_form import VersionModelForm

class TestRunForm(VersionModelForm):
    """
    Test Run form to allow user to select input parameters for a Backtest Run.
    """

    class Meta:
        model = TestRun
        # All other fields are updated by program, last_version is needed for optimistic locking
        fields = ['stock_ticker', 'start_date', 'end_date', 'portfolio_start', 'strategy_code', 'stop_loss',
                'indicator_1_code', 'ind_1_param_1', 'ind_1_param_2', 'ind_1_param_3',
                'indicator_2_code', 'ind_2_param_1', 'ind_2_param_2', 'ind_2_param_3',
                'trade_size', 'last_version' ]

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
