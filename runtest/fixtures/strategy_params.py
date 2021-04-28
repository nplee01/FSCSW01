import runtest.run_django
from runtest.fixtures.parameter import ParameterTuple, load_parameters
from runtest.fixtures.set_audit_user import set_audit_user

# Number of indicators allowed for Strategies (max is 3)
params = [
        ParameterTuple(param_code='1-IND', param_label='Max Indicators', 
            param_description='Max Indicators allowed for a Strategy', default_value=1,
            min_value=0, max_value=3, step_by=None, mult_by=None),
        ParameterTuple(param_code='2-IND', param_label='Max Indicators', 
            param_description='Max Indicators allowed for a Strategy', default_value=2,
            min_value=0, max_value=3, step_by=None, mult_by=None),
        ParameterTuple(param_code='3-IND', param_label='Max Indicators', 
            param_description='Max Indicators allowed for a Strategy', default_value=3,
            min_value=0, max_value=3, step_by=None, mult_by=None),
    ]
    
if __name__ == '__main__':
    set_audit_user()
    (ic, uc) = load_parameters(params)
    print("Strategy Parameters: Inserted: %d, Updated: %d" % (ic, uc))
