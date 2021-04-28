from django.test import TestCase, Client
from django.contrib.auth import get_user_model
User = get_user_model()

# For loading data
from runtest.fixtures.set_audit_user import set_audit_user
from runtest.fixtures.value_set import load_value_sets
from runtest.fixtures.parameter import load_parameters

# Data
from runtest.fixtures.stocks import stocks
from runtest.fixtures.strategy_params import params as stg_params
from runtest.fixtures.strategies import strategies
from runtest.fixtures.indicator_params import params as ind_params
from runtest.fixtures.indicators import indicators
from runtest.fixtures.run_params import params as run_params
from runtest.fixtures.run_fields import fields
from runtest.fixtures.size_params import params as size_params
from runtest.fixtures.size_methods import methods

from runtest.models import ValueSet

TESTUSER = 'tester'

class Test01(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create user for testing
        tu = User.objects.create_user(username=TESTUSER, password=TESTUSER, email=TESTUSER + '@atsc.org.my',
                is_active=True, is_staff=True, is_superuser=True)
        set_audit_user()
        # Load our fixtures. our load_fixtures.py when run out of process will load against the Dev DB
        # TestCase class will use a separate test DB for all fixtures
        # Stocks
        _unused = load_value_sets(stocks)
        # Strategies
        _unused = load_parameters(stg_params)
        _unused = load_value_sets(strategies)
        # Indicators
        _unused = load_parameters(ind_params)
        _unused = load_value_sets(indicators)
        # Run Fields
        _unused = load_parameters(run_params)
        _unused = load_value_sets(fields)
        # Size Methods
        _unused = load_parameters(size_params)
        _unused = load_value_sets(methods)

    def setUp(self):
        # For HTTP calls
        self.clt = Client()

    def test_stocks(self):
        # Ensure we have some stocks
        vs = ValueSet.objects.get(value_set_code='STOCKS')
        # Check out record owner trigger works
        self.assertEqual(vs.created_by, TESTUSER)
        # Check if get choices works
        ch = vs.get_choices() 
        self.assertGreater(len(ch), 0)

    def test_strategies(self):
        vs = ValueSet.objects.get(value_set_code='STRATEGIES')
        # Check out record owner trigger works
        self.assertEqual(vs.created_by, TESTUSER)
        ch = vs.get_choices() 
        self.assertGreater(len(ch), 0)
        # All strategies param 1 must have value
        for sm in vs.valuesetmember_set.all():
            self.assertIsNotNone(sm.param_1)
            # Its default value > 0
            self.assertGreater(sm.param_1.default_value, 0)

    def test_indicators(self):
        vs = ValueSet.objects.get(value_set_code='INDICATORS')
        # Check out record owner trigger works
        self.assertEqual(vs.created_by, TESTUSER)
        ch = vs.get_choices() 
        self.assertGreater(len(ch), 0)
        # All indicators must have at least 1 param
        for sm in vs.valuesetmember_set.all():
            self.assertIsNotNone(sm.param_1)
            # Its default value > 0
            self.assertGreater(sm.param_1.default_value, 0)

    def test_run_fields(self):
        vs = ValueSet.objects.get(value_set_code='RUN-FIELDS')
        # Check out record owner trigger works
        self.assertEqual(vs.created_by, TESTUSER)
        ch = vs.get_choices() 
        self.assertGreater(len(ch), 0)
        # All run fields must have at least 1 param
        for sm in vs.valuesetmember_set.all():
            self.assertIsNotNone(sm.param_1)
            # Its default value > 0
            self.assertGreater(sm.param_1.default_value, 0)

    def test_size_methods(self):
        vs = ValueSet.objects.get(value_set_code='SIZING-METHODS')
        # Check out record owner trigger works
        self.assertEqual(vs.created_by, TESTUSER)
        ch = vs.get_choices() 
        self.assertGreater(len(ch), 0)
        # All methods must have at least 1 param
        for sm in vs.valuesetmember_set.all():
            self.assertIsNotNone(sm.param_1)
            # Its default value > 0
            self.assertGreater(sm.param_1.default_value, 0)

    def test_rpc(self):
        # Get Run Params
        resp = self.clt.get('/runtest/rpc/GetRunParams', HTTP_ACCEPT='application/json')
        self.assertEqual(resp.status_code, 200)
        ret = resp.json()
        self.assertEqual(ret['status'], 'OK')
        self.assertIsNotNone(ret['data']['start_date'])
        self.assertGreater(ret['data']['portfolio_start'], 0)
        # Get Strategy Params
        resp = self.clt.get('/runtest/rpc/GetStrategyParams/CONFLUENCE', HTTP_ACCEPT='application/json')
        self.assertEqual(resp.status_code, 200)
        ret = resp.json()
        self.assertEqual(ret['status'], 'OK')
        self.assertGreater(ret['data']['indicator_count'], 0)
        # Get Indicator Params
        resp = self.clt.get('/runtest/rpc/GetIndicatorParams/RSI', HTTP_ACCEPT='application/json')
        self.assertEqual(resp.status_code, 200)
        ret = resp.json()
        self.assertEqual(ret['status'], 'OK')
        # Data is a list of params
        for pa in ret['data']:
            self.assertIsNotNone(pa['param_label'])
            self.assertGreater(pa['default_value'], 0)
        # Get Sizing Params
        resp = self.clt.get('/runtest/rpc/GetSizingParams/OVERLAP', HTTP_ACCEPT='application/json')
        self.assertEqual(resp.status_code, 200)
        ret = resp.json()
        self.assertEqual(ret['status'], 'OK')
        # Data is a list of params
        for pa in ret['data']:
            self.assertIsNotNone(pa['param_label'])
            self.assertGreater(pa['default_value'], 0)

    def test_views(self):
        # Home
        resp = self.clt.get('/')
        self.assertEqual(resp.status_code, 200)
        # About
        resp = self.clt.get('/about')
        self.assertEqual(resp.status_code, 200)
        # How it works
        resp = self.clt.get('/howitworks')
        self.assertEqual(resp.status_code, 200)
        # backtest
        resp = self.clt.get('/backtest')
        self.assertEqual(resp.status_code, 200)

    def test_admin(self):
        # Login as admin user
        self.assertTrue(self.clt.login(username=TESTUSER, password=TESTUSER))
        # Test our admins work
        resp = self.clt.get('/admin/runtest/parameter/') 
        self.assertEqual(resp.status_code, 200)
        resp = self.clt.get('/admin/runtest/valueset/') 
        self.assertEqual(resp.status_code, 200)
