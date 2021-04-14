import runtest.run_django
# When run as script, use absolute imports
from value_set import ValueSetTuple, SetMemberTuple, load_value_set
from set_audit_user import set_audit_user

if __name__ == '__main__':
    set_audit_user()
    # Misc run fields
    fields = [
        ValueSetTuple(value_set_code='RUN-FIELDS', value_set_description='Misc Fields for backtest run',
            set_member_list=(
                # Run range fields
                SetMemberTuple(value_code='RUN-RANGE', value_description='Run Range', sort_order=1,
                    param_1_code='RUN-START', param_2_code='RUN-END', param_3_code=None),
                SetMemberTuple(value_code='PORTFOLIO-START', value_description='Portfolio Start', sort_order=2,
                    param_1_code='PORTFOLIO-START', param_2_code=None, param_3_code=None),
                # used by strategy
                SetMemberTuple(value_code='STOP-LOSS', value_description='Stop Loss %', sort_order=3,
                    param_1_code='STOP-LOSS', param_2_code='TRAIL-STOP-LOSS', param_3_code=None),
            )
          )
        ]
    
    (ic, uc, mic, muc) = load_value_set(fields)
    print("Run Fields: Inserted: %d, Updated: %d" % (mic, muc))
