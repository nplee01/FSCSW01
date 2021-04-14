import runtest.run_django
# When run as script, use absolute imports
from parameter import ParameterTuple, load_parameters
from set_audit_user import set_audit_user

if __name__ == '__main__':
    set_audit_user()
    # Position Method Trade Size Params
    params = [
            ParameterTuple(param_code='OVL-SIZE', param_label='Trade Size', 
                param_description='Overlap Trade Size in Units', default_value=100,
                min_value=0, max_value=None, mult_by=None),
            ParameterTuple(param_code='FIXED-SIZE', param_label='Trade Size', 
                param_description='Fixed Trade Size in Units', default_value=100,
                min_value=0, max_value=None, mult_by=None),
            ParameterTuple(param_code='MAX-RISK-OVL', param_label='Trade Amount', 
                param_description='Max Risk Overlap Trade Amount', default_value=1000,
                min_value=0, max_value=None, mult_by=None),
            ParameterTuple(param_code='MAX-RISK-FIXED', param_label='Trade Amount', 
                param_description='Max Risk Fixed Trade Amount', default_value=1000,
                min_value=0, max_value=None, mult_by=None),
        ]
    
    (ic, uc) = load_parameters(params)
    print("Trade Size Parameters: Inserted: %d, Updated: %d" % (ic, uc))
