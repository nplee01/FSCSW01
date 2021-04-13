import runtest.run_django
# When run as script, use absolute imports
from value_set import ValueSetTuple, SetMemberTuple, load_value_set
from set_audit_user import set_audit_user

if __name__ == '__main__':
    set_audit_user()
    stocks = [
        ValueSetTuple(value_set_code='STOCKS', value_set_description='Stocks available for backtesting',
            set_member_list=(
                SetMemberTuple(value_code='6888', value_description='AXIATA', sort_order=1,
                    param_1=None, param_2=None, param_3=None),
                SetMemberTuple(value_code='1023', value_description='CIMB', sort_order=2,
                    param_1=None, param_2=None, param_3=None),
                SetMemberTuple(value_code='7277', value_description='DIALOG', sort_order=3,
                    param_1=None, param_2=None, param_3=None),
                SetMemberTuple(value_code='6947', value_description='DIGI', sort_order=4,
                    param_1=None, param_2=None, param_3=None),
                SetMemberTuple(value_code='3182', value_description='GENTING', sort_order=5,
                    param_1=None, param_2=None, param_3=None),
                SetMemberTuple(value_code='4715', value_description='GENM', sort_order=6,
                    param_1=None, param_2=None, param_3=None),
                SetMemberTuple(value_code='3034', value_description='HAPSENG', sort_order=7,
                    param_1=None, param_2=None, param_3=None),
                SetMemberTuple(value_code='5168', value_description='HARTALEGA', sort_order=8,
                    param_1=None, param_2=None, param_3=None),
                SetMemberTuple(value_code='5819', value_description='HONGLEONGBANK', sort_order=9,
                    param_1=None, param_2=None, param_3=None),
                SetMemberTuple(value_code='1082', value_description='HONGLEONGGROUP', sort_order=10,
                    param_1=None, param_2=None, param_3=None),
                SetMemberTuple(value_code='5225', value_description='IHH', sort_order=11,
                    param_1=None, param_2=None, param_3=None),
                SetMemberTuple(value_code='1961', value_description='IOI', sort_order=12,
                    param_1=None, param_2=None, param_3=None),
                SetMemberTuple(value_code='2445', value_description='KLK', sort_order=13,
                    param_1=None, param_2=None, param_3=None),
                SetMemberTuple(value_code='1155', value_description='MAYBANK', sort_order=14,
                    param_1=None, param_2=None, param_3=None),
                SetMemberTuple(value_code='6012', value_description='MAXIS', sort_order=15,
                    param_1=None, param_2=None, param_3=None),
                SetMemberTuple(value_code='3816', value_description='MISC', sort_order=16,
                    param_1=None, param_2=None, param_3=None),
                SetMemberTuple(value_code='4707', value_description='NESTLE', sort_order=17,
                    param_1=None, param_2=None, param_3=None),
                SetMemberTuple(value_code='5183', value_description='PCHEM', sort_order=18,
                    param_1=None, param_2=None, param_3=None),
                SetMemberTuple(value_code='5681', value_description='PDAGANG', sort_order=19,
                    param_1=None, param_2=None, param_3=None),
                SetMemberTuple(value_code='6033', value_description='PGAS', sort_order=20,
                    param_1=None, param_2=None, param_3=None),
                SetMemberTuple(value_code='4065', value_description='PPB', sort_order=21,
                    param_1=None, param_2=None, param_3=None),
                SetMemberTuple(value_code='8869', value_description='PMETAL', sort_order=22,
                    param_1=None, param_2=None, param_3=None),
                SetMemberTuple(value_code='1295', value_description='PUBLIC', sort_order=23,
                    param_1=None, param_2=None, param_3=None),
                SetMemberTuple(value_code='1066', value_description='RHB', sort_order=24,
                    param_1=None, param_2=None, param_3=None),
                SetMemberTuple(value_code='4197', value_description='SIMEDARBY', sort_order=25,
                    param_1=None, param_2=None, param_3=None),
                SetMemberTuple(value_code='5285', value_description='SIMEPLANT', sort_order=26,
                        param_1=None, param_2=None, param_3=None),
                SetMemberTuple(value_code='7106', value_description='SUPERMAX', sort_order=27,
                        param_1=None, param_2=None, param_3=None),
                SetMemberTuple(value_code='4863', value_description='TELEKOM', sort_order=28,
                        param_1=None, param_2=None, param_3=None),
                SetMemberTuple(value_code='5347', value_description='TENAGA', sort_order=29,
                        param_1=None, param_2=None, param_3=None),
                SetMemberTuple(value_code='7113', value_description='TOPGLOVE', sort_order=30,
                        param_1=None, param_2=None, param_3=None),
                )
            )
        ]
    
    (ic, uc, mic, muc) = load_value_set(stocks)
    print("Value Sets: Inserted: %d, Updated: %d, Members Inserted: %d, Members Updated: %d" %
        (ic, uc, mic, muc))
