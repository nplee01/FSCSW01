from copy import deepcopy

import runtest.run_django
from runtest.fixtures.parameter import ParameterTuple, load_parameters
from runtest.fixtures.set_audit_user import set_audit_user
from runtest.models import ValueSet, ValueSetMember, Parameter
# Load this AFTER stocks.py as we need to read its data

# Download start and end dates by stock
# 1st download will set start date with earliest price data 
P1_CODE='DOWNLOAD-START'
P2_CODE='DOWNLOAD-END'
def create_params():
    start_tuple = ParameterTuple(param_code=P1_CODE, param_label='Download Start Date', 
            param_description='Start Date as ordinal number', default_value=None, 
            min_value=0, max_value=None, step_by=None, mult_by=None)
    end_tuple = ParameterTuple(param_code=P2_CODE, param_label='Download End Date', 
            param_description='End Date as ordinal number', default_value=None, # as at last download date
            min_value=0, max_value=None, step_by=None, mult_by=None)

    params = []
    vs = ValueSet.objects.get(value_set_code='STOCKS')
    for stock, stock_name in [(st.value_code, st.value_description) for 
        st in ValueSetMember.objects.filter(value_set=vs)]:
        st = deepcopy(start_tuple)
        st = st._replace(param_code=stock_name + '-' + P1_CODE)
        params.append(st)
        ed = deepcopy(end_tuple)
        ed = ed._replace(param_code=stock_name + '-' + P2_CODE)
        params.append(ed)

    return params

def update_stocks():
    # Update the stock params 1 and 2 to download dates
    vs = ValueSet.objects.get(value_set_code='STOCKS')
    for stock in ValueSetMember.objects.filter(value_set=vs):
        p1 = Parameter.objects.get(param_code=stock.value_description + '-' + P1_CODE)
        p2 = Parameter.objects.get(param_code=stock.value_description + '-' + P2_CODE)
        stock.param_1 = p1
        stock.param_2 = p2
        stock.save()
    
if __name__ == '__main__':
    set_audit_user()
    params = create_params()
    (ic, uc) = load_parameters(params)
    print("Stock Parameters: Inserted: %d, Updated: %d" % (ic, uc))
    update_stocks()
