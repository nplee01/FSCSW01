import runtest.run_django
from runtest.fixtures.value_set import ValueSetTuple, SetMemberTuple, load_value_sets
from runtest.fixtures.set_audit_user import set_audit_user

# Indicators allowed. Up to 3 params allowed per Indicator
indicators = [
    ValueSetTuple(value_set_code='INDICATORS', value_set_description='Indicators for backtesting',
        set_member_list=(
            # Version 1.0 data
            # SetMemberTuple(value_code='BUYNHOLD', value_description='Buy and Hold', sort_order=1,
            #     param_1_code=None, param_2_code=None, 
            #     param_3_code=None, param_4_code=None, param_5_code=None),
            SetMemberTuple(value_code='SMA', value_description='SMA as Baseline', sort_order=2,
                param_1_code='SMA-BASE-LINE', param_2_code=None, param_3_code=None,
                param_4_code=None, param_5_code=None),
            SetMemberTuple(value_code='XMA', value_description='SMA Crossing', sort_order=3,
                param_1_code='XMA-FAST-PERIOD', param_2_code='XMA-SLOW-PERIOD', param_3_code=None,
                param_4_code=None, param_5_code=None),
            SetMemberTuple(value_code='RSIOBOS', value_description='RSI OB/OS', sort_order=4,
                param_1_code='RSI-PERIOD', param_2_code='RSI-OVERBOT', param_3_code='RSI-BASE-LINE',
                param_4_code='RSI-OVERSOLD', param_5_code=None),
            )
        )
    ]
    
if __name__ == '__main__':
    set_audit_user()
    (ic, uc, mic, muc) = load_value_sets(indicators)
    print("Indicators: Inserted: %d, Updated: %d" % (mic, muc))
    """ Version 0.0 data
                SetMemberTuple(value_code='RSI', value_description='RSI', sort_order=1,
                    param_1_code='RSI-PERIOD', param_2_code='RSI-LOW-BAND', param_3_code='RSI-UP-BAND'),
                SetMemberTuple(value_code='SMA-X', value_description='SMA Crossover', sort_order=2,
                    param_1_code='SMAX-FAST-PERIOD', param_2_code='SMAX-SLOW-PERIOD', param_3_code=None),
                SetMemberTuple(value_code='WMA-C', value_description='WMA Continuous', sort_order=3,
                    param_1_code='WMAC-P1', param_2_code=None, param_3_code=None),
                SetMemberTuple(value_code='CKO', value_description='Chaikin Oscillator', sort_order=4,
                    param_1_code='CKO-PERIOD', param_2_code='CKO-FAST-EMA', param_3_code='CKO-SLOW-EMA'),
                SetMemberTuple(value_code='ART', value_description='Aroon Trend', sort_order=5,
                    param_1_code='ART-PERIOD', param_2_code=None, param_3_code=None),
                SetMemberTuple(value_code='BLB', value_description='Bollinger Bands', sort_order=6,
                    param_1_code='BLB-PERIOD', param_2_code=None, param_3_code=None),
                SetMemberTuple(value_code='ARX', value_description='Aroon Crossover', sort_order=7,
                    param_1_code='ARX-PERIOD', param_2_code='ARX-LOW-BAND', param_3_code='ARX-UP-BAND'),
                SetMemberTuple(value_code='MACD-X', value_description='MACD Crossover', sort_order=8,
                    param_1_code='MACX-FAST-PERIOD', param_2_code='MACX-SLOW-PERIOD', 
                    param_3_code='MACX-SIGNAL-PERIOD'),
                SetMemberTuple(value_code='HLR', value_description='High Low Reversion', sort_order=9,
                    param_1_code='HLR-PERIOD', param_2_code=None, param_3_code=None),
                SetMemberTuple(value_code='HLT', value_description='High Low Trending', sort_order=10,
                    param_1_code='HLT-PERIOD', param_2_code=None, param_3_code=None),
                SetMemberTuple(value_code='WMA-X', value_description='WMA Crossover', sort_order=11,
                    param_1_code='WMAX-FAST-PERIOD', param_2_code='WMAX-SLOW-PERIOD', param_3_code=None),
                SetMemberTuple(value_code='CCI', value_description='CCI', sort_order=12,
                    param_1_code='CCI-PERIOD', param_2_code='CCI-LOW-BAND', param_3_code='CCI-UP-BAND'),
                SetMemberTuple(value_code='ADX-X', value_description='ADX Crossover', sort_order=13,
                    param_1_code='ADXX-PERIOD', param_2_code='ADXX-STRENGTH', param_3_code=None),
                SetMemberTuple(value_code='STX', value_description='Stochastic Crossover', sort_order=14,
                    param_1_code='STX-PERIOD', param_2_code='STX-LOW-BAND', param_3_code='STX-UP-BAND'),
                SetMemberTuple(value_code='STO', value_description='Stochastic Oscillator', sort_order=15,
                    param_1_code='STO-PERIOD', param_2_code='STO-LOW-BAND', param_3_code='STO-UP-BAND'),
                SetMemberTuple(value_code='SMA', value_description='SMA', sort_order=16,
                    param_1_code='SMA-PERIOD', param_2_code=None, param_3_code=None),
                SetMemberTuple(value_code='SMA-C', value_description='SMA Continuous', sort_order=17,
                    param_1_code='SMAC-P1', param_2_code=None, param_3_code=None),
                SetMemberTuple(value_code='EMA', value_description='EMA', sort_order=18,
                    param_1_code='EMA-PERIOD', param_2_code=None, param_3_code=None),
                SetMemberTuple(value_code='EMA-C', value_description='EMA Continuous', sort_order=19,
                    param_1_code='EMAC-P1', param_2_code=None, param_3_code=None),
    """
    """
            # Version 0.1 data
            SetMemberTuple(value_code='MACD', value_description='MACD', sort_order=1,
                param_1_code='MAC-FAST-PERIOD', param_2_code='MAC-SLOW-PERIOD', 
                param_3_code='MAC-SIGNAL-PERIOD', param_4_code=None, param_5_code=None),
            SetMemberTuple(value_code='BLB', value_description='Bollinger Bands', sort_order=2,
                param_1_code='BLB-PERIOD', param_2_code=None, param_3_code=None,
                param_4_code=None, param_5_code=None),
            SetMemberTuple(value_code='EMA', value_description='EMA', sort_order=3,
                param_1_code='EMA-PERIOD', param_2_code=None, param_3_code=None,
                param_4_code=None, param_5_code=None),
            SetMemberTuple(value_code='RSI', value_description='RSI', sort_order=4,
                param_1_code='RSI-PERIOD', param_2_code='RSI-LOW-BAND', param_3_code='RSI-UP-BAND',
                param_4_code=None, param_5_code=None),
    """

