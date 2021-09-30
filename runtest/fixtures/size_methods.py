import runtest.run_django
from runtest.fixtures.value_set import ValueSetTuple, SetMemberTuple, load_value_sets
from runtest.fixtures.set_audit_user import set_audit_user

# Sizing Methods allowed for trading (NOT USED)
methods = [
    ValueSetTuple(value_set_code='SIZING-METHODS', value_set_description='Sizing Methods for Trading',
         set_member_list=(
             SetMemberTuple(value_code='OVERLAP', value_description='Overlap', sort_order=1,
                 param_1_code='OVL-SIZE', param_2_code=None, param_3_code=None,
                 param_4_code=None, param_5_code=None),
             SetMemberTuple(value_code='FIXED', value_description='Fixed', sort_order=2,
                 param_1_code='FIXED-SIZE', param_2_code=None, param_3_code=None,
                 param_4_code=None, param_5_code=None),
             SetMemberTuple(value_code='MAX-RISK-OVERLAP', value_description='Max Risk (Overlap)', sort_order=3,
                 param_1_code='MAX-RISK-OVL', param_2_code=None, param_3_code=None,
                 param_4_code=None, param_5_code=None),
             SetMemberTuple(value_code='MAX-RISK-FIXED', value_description='Max Risk (Fixed)', sort_order=4,
                 param_1_code='MAX-RISK-FIXED', param_2_code=None, param_3_code=None,
                 param_4_code=None, param_5_code=None),
            )
         )
    ]
    
if __name__ == '__main__':
    set_audit_user()
    (ic, uc, mic, muc) = load_value_sets(methods)
    print("Sizing Methods: Inserted: %d, Updated: %d" % (mic, muc))
