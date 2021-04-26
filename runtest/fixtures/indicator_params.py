import runtest.run_django
# When run as script, use absolute imports
from parameter import ParameterTuple, load_parameters
from set_audit_user import set_audit_user

if __name__ == '__main__':
    set_audit_user()
    params = [
            # Version 0.1 data
            # MACD 
            ParameterTuple(param_code='MAC-FAST-PERIOD', param_label='Faster Period', 
                param_description='MACD Faster Period', default_value=12,
                min_value=0, max_value=None, step_by=None, mult_by=None),
            ParameterTuple(param_code='MAC-SLOW-PERIOD', param_label='Slower Period', 
                param_description='MACD Slower Period', default_value=26,
                min_value=0, max_value=None, step_by=None, mult_by=None),
            ParameterTuple(param_code='MAC-SIGNAL-PERIOD', param_label='Signal Period', 
                param_description='MACD Signal Period', default_value=9,
                min_value=0, max_value=None, step_by=None, mult_by=None),
            # Bollinger Bands
            ParameterTuple(param_code='BLB-PERIOD', param_label='Period', 
                param_description='Bollinger Bands Period', default_value=20,
                min_value=0, max_value=None, step_by=None, mult_by=None),
            # EMA
            ParameterTuple(param_code='EMA-PERIOD', param_label='Period', 
                param_description='EMA Period', default_value=14,
                min_value=0, max_value=None, step_by=None, mult_by=None),
            # RSI
            ParameterTuple(param_code='RSI-PERIOD', param_label='Period', 
                param_description='RSI Period', default_value=14,
                min_value=0, max_value=None, step_by=None, mult_by=None),
            ParameterTuple(param_code='RSI-LOW-BAND', param_label='Lower Band', 
                param_description='RSI Lower Band', default_value=30,
                min_value=None, max_value=None, step_by=None, mult_by=None),
            ParameterTuple(param_code='RSI-UP-BAND', param_label='Upper Band', 
                param_description='RSI Upper Band', default_value=70,
                min_value=None, max_value=None, step_by=None, mult_by=None),
        ]
    
    (ic, uc) = load_parameters(params)
    print("Indicator Parameters: Inserted: %d, Updated: %d" % (ic, uc))
    """
            # RSI
            ParameterTuple(param_code='RSI-PERIOD', param_label='Period', 
                param_description='RSI Period', default_value=14,
                min_value=None, max_value=None, step_by=None, mult_by=None),
            ParameterTuple(param_code='RSI-LOW-BAND', param_label='Lower Band', 
                param_description='RSI Lower Band', default_value=30,
                min_value=None, max_value=None, step_by=None, mult_by=None),
            ParameterTuple(param_code='RSI-UP-BAND', param_label='Upper Band', 
                param_description='RSI Upper Band', default_value=70,
                min_value=None, max_value=None, step_by=None, mult_by=None),
            # SMA Crossover
            ParameterTuple(param_code='SMAX-FAST-PERIOD', param_label='Faster Period', 
                param_description='SMA Crossover Faster Period', default_value=12,
                min_value=None, max_value=None, step_by=None, mult_by=None),
            ParameterTuple(param_code='SMAX-SLOW-PERIOD', param_label='Slower Period', 
                param_description='SMA Crossover Slower Period', default_value=26,
                min_value=None, max_value=None, step_by=None, mult_by=None),
            # WMA Continuous
            ParameterTuple(param_code='WMAC-P1', param_label='p1', 
                param_description='WMA Continuous Param 1', default_value=14,
                min_value=None, max_value=None, step_by=None, mult_by=None),
            # Chaikin Oscillator
            ParameterTuple(param_code='CKO-PERIOD', param_label='Period', 
                param_description='Chaikin Oscillator Period', default_value=20,
                min_value=None, max_value=None, step_by=None, mult_by=None),
            ParameterTuple(param_code='CKO-FAST-EMA', param_label='Faster EMA', 
                param_description='Chaikin Oscillator Faster EMA', default_value=3,
                min_value=None, max_value=None, step_by=None, mult_by=None),
            ParameterTuple(param_code='CKO-SLOW-EMA', param_label='Slower EMA', 
                param_description='Chaikin Oscillator Slower EMA', default_value=10,
                min_value=None, max_value=None, step_by=None, mult_by=None),
            # Aroon Trend
            ParameterTuple(param_code='ART-PERIOD', param_label='Period', 
                param_description='Aroon Trend Period', default_value=25,
                min_value=None, max_value=None, step_by=None, mult_by=None),
            # Bollinger Bands
            ParameterTuple(param_code='BLB-PERIOD', param_label='Period', 
                param_description='Bollinger Bands Period', default_value=20,
                min_value=None, max_value=None, step_by=None, mult_by=None),
            # Aroon Crossover
            ParameterTuple(param_code='ARX-PERIOD', param_label='Period', 
                param_description='Aroon Crossover Period', default_value=25,
                min_value=None, max_value=None, step_by=None, mult_by=None),
            ParameterTuple(param_code='ARX-LOW-BAND', param_label='Lower Band', 
                param_description='Aroon Crossover Lower Band', default_value=30,
                min_value=None, max_value=None, step_by=None, mult_by=None),
            ParameterTuple(param_code='ARX-UP-BAND', param_label='Upper Band', 
                param_description='Aroon Crossover Upper Band', default_value=70,
                min_value=None, max_value=None, step_by=None, mult_by=None),
            # MACD Crossover
            ParameterTuple(param_code='MACX-FAST-PERIOD', param_label='Faster Period', 
                param_description='MACD Crossover Faster Period', default_value=12,
                min_value=None, max_value=None, step_by=None, mult_by=None),
            ParameterTuple(param_code='MACX-SLOW-PERIOD', param_label='Slower Period', 
                param_description='MACD Crossover Slower Period', default_value=26,
                min_value=None, max_value=None, step_by=None, mult_by=None),
            ParameterTuple(param_code='MACX-SIGNAL-PERIOD', param_label='Signal Period', 
                param_description='MACD Crossover Signal Period', default_value=9,
                min_value=None, max_value=None, step_by=None, mult_by=None),
            # High Low Reversion
            ParameterTuple(param_code='HLR-PERIOD', param_label='Period', 
                param_description='High Low Reversion Period', default_value=20,
                min_value=None, max_value=None, step_by=None, mult_by=None),
            # High Low Trending
            ParameterTuple(param_code='HLT-PERIOD', param_label='Period', 
                param_description='High Low Trending Period', default_value=20,
                min_value=None, max_value=None, step_by=None, mult_by=None),
            # WMA Crossover
            ParameterTuple(param_code='WMAX-FAST-PERIOD', param_label='Faster Period', 
                param_description='WMA Crossover Faster Period', default_value=12,
                min_value=None, max_value=None, step_by=None, mult_by=None),
            ParameterTuple(param_code='WMAX-SLOW-PERIOD', param_label='Slower Period', 
                param_description='WMA Crossover Slower Period', default_value=26,
                min_value=None, max_value=None, step_by=None, mult_by=None),
            # CCI
            ParameterTuple(param_code='CCI-PERIOD', param_label='Period', 
                param_description='CCI Period', default_value=20,
                min_value=None, max_value=None, step_by=None, mult_by=None),
            ParameterTuple(param_code='CCI-LOW-BAND', param_label='Lower Band', 
                param_description='CCI Lower Band', default_value=-100,
                min_value=None, max_value=None, step_by=None, mult_by=None),
            ParameterTuple(param_code='CCI-UP-BAND', param_label='Upper Band', 
                param_description='CCI Upper Band', default_value=100,
                min_value=None, max_value=None, step_by=None, mult_by=None),
            # ADX Crossover
            ParameterTuple(param_code='ADXX-PERIOD', param_label='Period', 
                param_description='ADX Crossover Period', default_value=14,
                min_value=None, max_value=None, step_by=None, mult_by=None),
            ParameterTuple(param_code='ADXX-STRENGTH', param_label='Strength', 
                param_description='ADX Crossover Strength', default_value=25,
                min_value=None, max_value=None, step_by=None, mult_by=None),
            # Stochastic Crossover
            ParameterTuple(param_code='STX-PERIOD', param_label='Period', 
                param_description='Stochastic Crossover Period', default_value=14,
                min_value=None, max_value=None, step_by=None, mult_by=None),
            ParameterTuple(param_code='STX-LOW-BAND', param_label='Lower Band', 
                param_description='Stochastic Crossover Lower Band', default_value=20,
                min_value=None, max_value=None, step_by=None, mult_by=None),
            ParameterTuple(param_code='STX-UP-BAND', param_label='Upper Band', 
                param_description='Stochastic Crossover Upper Band', default_value=80,
                min_value=None, max_value=None, step_by=None, mult_by=None),
            # Stochastic Oscillator
            ParameterTuple(param_code='STO-PERIOD', param_label='Period', 
                param_description='Stochastic Oscillator Period', default_value=14,
                min_value=None, max_value=None, step_by=None, mult_by=None),
            ParameterTuple(param_code='STO-LOW-BAND', param_label='Lower Band', 
                param_description='Stochastic Oscillator Lower Band', default_value=20,
                min_value=None, max_value=None, step_by=None, mult_by=None),
            ParameterTuple(param_code='STO-UP-BAND', param_label='Upper Band', 
                param_description='Stochastic Oscillator Upper Band', default_value=80,
                min_value=None, max_value=None, step_by=None, mult_by=None),
            # SMA
            ParameterTuple(param_code='SMA-PERIOD', param_label='Period', 
                param_description='SMA Period', default_value=14,
                min_value=None, max_value=None, step_by=None, mult_by=None),
            # SMA Continuous
            ParameterTuple(param_code='SMAC-P1', param_label='p1', 
                param_description='SMA Continuous Param 1', default_value=14,
                min_value=None, max_value=None, step_by=None, mult_by=None),
            # EMA
            ParameterTuple(param_code='EMA-PERIOD', param_label='Period', 
                param_description='EMA Period', default_value=14,
                min_value=None, max_value=None, step_by=None, mult_by=None),
            # EMA Continuous
            ParameterTuple(param_code='EMAC-P1', param_label='p1', 
                param_description='EMA Continuous Param 1', default_value=14,
                min_value=None, max_value=None, step_by=None, mult_by=None),
    """

