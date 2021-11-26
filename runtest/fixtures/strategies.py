import runtest.run_django
from runtest.fixtures.value_set import ValueSetTuple, SetMemberTuple, load_value_sets
from runtest.fixtures.set_audit_user import set_audit_user

# Strategies allowed. Parameters like stop_loss and levels hardcoded
# Param 1 is number of Indicators allowed (max 3)
strategies = [
    ValueSetTuple(value_set_code='STRATEGIES', value_set_description='Strategies for backtesting',
        # Version 0.1 data
        set_member_list=(
            SetMemberTuple(value_code='SINGLE', value_description='Single Indicator', sort_order=1,
                param_1_code='1-IND', param_2_code=None, param_3_code=None,
                param_4_code=None, param_5_code=None),
            )
        )
    ]
    
if __name__ == '__main__':
    set_audit_user()
    (ic, uc, mic, muc) = load_value_sets(strategies)
    print("Strategies: Inserted: %d, Updated: %d" % (mic, muc))

    """ Version 0.0 data
                SetMemberTuple(value_code='ONE-SHOT', value_description='One Shot', sort_order=1,
                    param_1_code='1-IND', param_2_code=None, param_3_code=None,
                    param_4_code=None, param_5_code=None),
                SetMemberTuple(value_code='KILL-SWITCH', value_description='Kill Switch', sort_order=2,
                    param_1_code='2-IND', param_2_code=None, param_3_code=None,
                    param_4_code=None, param_5_code=None),
                SetMemberTuple(value_code='DOUBLE-BARREL', value_description='Double Barrel', sort_order=3,
                    param_1_code='2-IND', param_2_code=None, param_3_code=None,
                    param_4_code=None, param_5_code=None),
                SetMemberTuple(value_code='CONFLUENCE', value_description='Confluence', sort_order=4,
                    param_1_code='2-IND', param_2_code=None, param_3_code=None,
                    param_4_code=None, param_5_code=None),
                SetMemberTuple(value_code='HIERARCHY', value_description='Hierarchy', sort_order=5,
                    param_1_code='2-IND', param_2_code=None, param_3_code=None,
                    param_4_code=None, param_5_code=None),
    """
