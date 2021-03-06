import runtest.run_django
from runtest.fixtures.parameter import ParameterTuple, load_parameters
from runtest.fixtures.set_audit_user import set_audit_user

# Misc run fields to default
params = [
        # Run start used as initial download date
        ParameterTuple(param_code='RUN-START', param_label='Start Date', 
            param_description='Start Date as ordinal number', default_value=730122, # is 2000-01-03
            min_value=0, max_value=None, step_by=None, mult_by=None),
        ParameterTuple(param_code='RUN-END', param_label='End Date', 
            param_description='End Date as ordinal number', default_value=None, # as at last download date
            min_value=0, max_value=None, step_by=None, mult_by=None),
        ParameterTuple(param_code='PORTFOLIO-START', param_label='Initial Capital', 
            param_description='Portfolio Initial Capital', default_value=10000,
            min_value=0, max_value=None, step_by=1000, mult_by=None),
        ParameterTuple(param_code='STOP-LOSS', param_label='Stop Loss %', 
            param_description='Stop Loss %', default_value=5,
            min_value=0, max_value=100, step_by=None, mult_by=0.01),
        ParameterTuple(param_code='TRADE-SIZE', param_label='Trade Size',
            param_description='Trade Size', default_value=1000,
            min_value=0, max_value=None, step_by=None, mult_by=None),
        # ParameterTuple(param_code='TRAIL-STOP-LOSS', param_label='Trailing Stop Loss %', 
        #     param_description='Trailing Stop Loss %', default_value=10,
        #     min_value=0, max_value=None, step_by=None, mult_by=0.01),
    ]
    
if __name__ == '__main__':
    set_audit_user()
    (ic, uc) = load_parameters(params)
    print("Run Parameters: Inserted: %d, Updated: %d" % (ic, uc))
